from flask import request
from flask_restful import Resource
from marshmallow import ValidationError

from application.models.event import EventModel
from application.models.participant import ParticipantModel
from application.models.team import TeamModel
from application.models.payment import PaymentModel
from application.error_handlers import *
from application.schemas import EventRegistration, TeamSchema, EventSchema
from application.mailer import Mailer


class EventRegister(Resource):
    """Handle event registrations for teams/participants"""

    def post(self, event_id):
        """register participants under an event
        handles user creation, team creation and mapping in one place"""

        # parse data
        er_schema = EventRegistration()
        try:
            data = er_schema.load(request.get_json())
        except ValidationError as err:
            return err.messages, 400

        event = EventModel.find_by_id(event_id)
        if not event:
            raise NotFound(message="The event does not exist")

        # check if the event is consistent with number of participants
        # under a team
        if not event.team_participation and len(data["participants"]) > 1:
            raise BadRequest(
                message="The event does not allow team participation. Should \
                     be only one member under a team"
            )

        # validate the participants
        self.validate_or_create_participants(data["participants"], event)

        # create a team
        team = self.create_team(
            data["team_name"],
            not event.team_participation,
            event_id,
            data["participation_level"],
        )

        # create a payment record for the corresponding team
        payment = self.create_payment(team.id)

        # add participants to the corresponding team and event
        self.map_participants(data["participants"], event, team)

        # send participation email to the first participant
        mailer = Mailer()
        mailer.send_participation_mail(
            data["participants"][0]["email"], event, team.team_identifier
        )

        return (
            TeamSchema(only=("id", "name", "team_identifier")).dump(team),
            201,
        )

    def validate_or_create_participants(self, participants, event):
        for participant in participants:
            # find the user
            participant_obj = ParticipantModel.find_by_email(
                participant["email"]
            )

            # if exists, check if he has already participated in the event
            if participant_obj and participant_obj.has_participated_event(
                event.id
            ):
                raise BadRequest(
                    message='The email "{email}" is already registered under \
                        event "{event}"'.format(
                        email=participant["email"], event=event.name
                    )
                )
            elif participant_obj is None:
                # the participant does not exist, so create a new one
                self.create_participant(
                    participant["name"],
                    participant["email"],
                    participant["tshirt_size"],
                    participant["institute"],
                    participant["contact_no"],
                )

    def map_participants(self, participants, event, team):
        """Assign participants to a particular team & a particular event"""

        for participant in participants:
            participant_obj = ParticipantModel.find_by_email(
                participant["email"]
            )

            # update fields that were previously missing
            updated = False
            for attr, value in participant.items():
                if not getattr(participant_obj, attr):
                    setattr(participant_obj, attr, value)
                    updated = True
            if updated:
                participant_obj.save()

            event.add_participant(participant_obj)
            team.add_participant(participant_obj)

    def create_participant(
        self, name, email, tshirt_size, institute, contact_no
    ):
        participant_obj = ParticipantModel(
            name, email, tshirt_size, institute, contact_no
        )
        participant_obj.save()
        return participant_obj

    def create_team(self, name, single, event_id, participation_level):
        team = TeamModel(name, single, event_id, participation_level)
        team.save()
        return team

    def create_payment(self, team_id):
        payment = PaymentModel(team_id)
        payment.save()
        return payment

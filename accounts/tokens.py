from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type


class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
	def _make_hash_value(self, user, timestamp):
		return (
				text_type(user.pk) + text_type(timestamp) + text_type(user.customerprofile.email_confirmed)
			)
account_activation_token = AccountActivationTokenGenerator()


class AgentAccountActivationGenerator(PasswordResetTokenGenerator):
	def _make_hash_value(self, user, timestamp):
		return (
			text_type(user.pk) + text_type(timestamp) + text_type(user.agentprofile.email_confirmed)
			)
agent_account_activation = AgentAccountActivationGenerator()
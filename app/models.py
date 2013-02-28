from app import db

class Contact(db.Model):
	contact_id = db.Column(db.String(50), primary_key=True)
	contact_name = db.Column(db.String(50))
	contact_email = db.Column(db.String(50))
	message = db.Column(db.Text)

	# data transfer object to form JSON
	def dto(self):
		return dict(
				contact_id = self.contact_id,
				contact_name = self.contact_name,
				contact_email = self.contact_email,
				message = self.message)

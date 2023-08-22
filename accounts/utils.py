def detectUser(user):
	if user.role == 1:
		redirectUrl = 'vendorDashboard'
	elif user.role == 2:
		redirectUrl = 'customerDashboard'
	else:
		redirectUrl = '/admin'

	return redirectUrl
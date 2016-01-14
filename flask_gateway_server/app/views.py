from app import app
from flask import request
import xmltodict
from app import db, models
import time








def process_controller(device, mode, global_params):
	""" Processes a controller configuration command and configures a db controller
	:param device: device configuration dictionary structure
	:returns: "OK" or an error message
	"""

	try:
		dev_id = device['@id']
		dev_ctrlId = device['@ctrlId']
		# dev_networkId = device['@networkId']
		dev_type = device['@type']
	except:
		print "some wrong device configuration"
		resp = "Error: Bad device id/ctrlId/type data"
		return resp
	
	db_controller = models.Controller.query.all()
	if len(db_controller)>1:
		return error
	
	if mode == 'COMPLETE' and len(db_controller)==1:
		db.session.delete(db_controller[0])
		db_controller = models.Controller()
		db.session.add(db_controller)

	elif mode == 'COMPLETE' and len(db_controller)==0:
		db_controller = models.Controller()
		db.session.add(db_controller[0])

	elif mode == 'UPDATE' and len(db_controller)==0:
		return error

	elif mode == 'UPDATE':
		db_controller = db_controller[0]
	
			
	# Retrivieng parameters to set
	if type(device['params']['param']) is list:
		params = device['params']['param']
	else:
		params = [device['params']['param']]	
	
	param_dict = {}
	for param in params:
		param_dict[param['@key']] = param['#text']

	# Configure the controller
	try:
		print "\nConfiguring ", dev_type, " device id:", dev_id, " on controller:", dev_ctrlId, " parameters:"
		for k in param_dict.keys():
			# Log
			print "Setting ", k, " to ", param_dict[k]
			db_controller.k = param_dict[k]
			
	except:
		db.session.rollback()
		return 'Error: Failed to set attribute ', k, ' to controller ', dev_id, ':', dev_ctrlId, ' - rolling back'
	
	db.session.commit()
	return 'OK'







def process_streetlight(device, mode, global_params):
	""" Processes a strretlight configuration command and configures a db strretlight
	:param device: device configuration dictionary structure
	:returns: "OK" or an error message
	"""

	try:
		dev_id = device['@id']
		dev_ctrlId = device['@ctrlId']
		# dev_networkId = device['@networkId']
		dev_type = device['@type']
	except:
		print "Error: Bad device id/ctrlId/type data"
		return "Error: Bad device id/ctrlId/type data"
	
	db_controller = models.Controller.query.all()
	if len(db_controller)>1:
		return "Error: To many controllers defined in the system"
	
	if mode == 'COMPLETE':
		db_streetlight = models.Streetlight()
		db.session.add(db_streetlight)

	elif mode == 'UPDATE':
		db_streetlight = db.session.query(Streetlight).filter(Streetlight.controllerStrId==dev_ctrlId).filter(Streetlight.idOnController==dev_id)
		if len(db_streetlight)>1:
			return 'Error: More than one identical streetlight devices present in the system'
		elif len(db_streetlight)==1:
			db_streetlight = db_streetlight[0]
		else:
			db_streetlight = models.Streetlight()
			db.session.add(db_streetlight)
	
			
	# Retrivieng parameters to set
	if type(device['params']['param']) is list:
		params = device['params']['param']
	else:
		params = [device['params']['param']]	
	
	param_dict = {}
	for param in params:
		param_dict[param['@key']] = param['#text']

	# Configure the streetlight
	try:
		print "\nConfiguring ", dev_type, " device id:", dev_id, " on controller:", dev_ctrlId, " parameters:"
		for k in param_dict.keys():
			# Log
			print "Setting ", k, " to ", param_dict[k]
			db_controller.k = param_dict[k]
			
	except:
		db.session.rollback()
		return 'Error: Failed to set attribute ', k, ' to streetlight ', dev_id, ':', dev_ctrlId, ' - rolling back'
	
	db.session.commit()
	return 'OK'

def parse_configuration(payload):
	""" Parses a configuration command and configures a devices
	:param payload: configuration dictionary structure
	:returns: "OK" or an error message
	"""
	ctrl_defined = False
	controller_defined_or_updated = True
	errors = []

	response = {}
	config = payload['configuration']
	ctrlId = config['@ctrlId']

	# Check if one controller is defined in the system
	db_controllers = models.Controller.query.all()
	# The controller is defined in the system
	if len(db_controllers)==1:
		print "One controller is defined in the system"
		ctrl_defined = True
		controller = db_controllers[0]
		# Wrong ctrlId
		if controller.controllerStrId != ctrlId:
			errors.append("Error: configuration ctrlId doesn't match this controller controllerStrId")
			print "Error: configuration ctrlId doesn't match this controller controllerStrId" 
			return errors	
	elif len(db_controllers)>1:
		errors.append("Error: to many controllers are defined in the system")
		print "Error: to many controllers are defined in the system" 
		return errors
	
	# Checking configuration structure

	conf_devices = []
	conf_devices_streetlight = []
	conf_devices_controller = []
	conf_devices_other = []
	conf_global_params = []
	conf_resources = []
	conf_programs = []
	conf_calendars = []
	dev_mode=""
	schedulers_mode=""

	if 'devices' in config.keys():
		dev_mode = config['devices']['@mode']
		# Checking devices
		if 'device' in config['devices'].keys():
			if type(config['devices']['device']) is list:
				conf_devices = config['devices']['device']
			else:
				conf_devices = [config['devices']['device']]
		
		for dev in conf_devices:
			if dev['@type'] == 'controller':
				conf_devices_controller.append(dev)
			elif dev['@type'] == 'streetlight':
				conf_devices_streetlight.append(dev)
			else:
				conf_devices_other.append(dev)

		# Checking resources
		if 'resource' in config['devices'].keys():
			if type(config['devices']['resource']) is list:
				conf_resources = config['devices']['resource']
			else:
				conf_resourses = [config['devices']['resource']]

		# Checking global configuration parameters
		if 'params' in config['devices'].keys() and 'param' in config['devices']['params'].keys():
			if type(config['devices']['params']['param']) is list:
				conf_global_params = config['devices']['params']['param']
			else:
				conf_global_params = [config['devices']['params']['param']]

	
	
	if 'schedulers' in config.keys():
		schedulers_mode = config['schedulers']['@mode']
		# Checking control programs
		if 'controlPrograms' in config['schedulers'].keys() and 'controlProgram' in config['schedulers']['controlPrograms'].keys():
			if type(config['schedulers']['controlPrograms']['controlProgram']) is list:
				conf_programs = config['schedulers']['controlPrograms']['controlProgram']
			else:
				conf_programs = [config['schedulers']['controlPrograms']['controlProgram']]
		
		# Checking calendars
		if 'calendars' in config['schedulers'].keys() and 'calendar' in config['schedulers']['calendars'].keys():
			if type(config['schedulers']['calendars']['calendar']) is list:
				conf_calendars = config['schedulers']['calendars']['calendar']
			else:
				conf_calendars = [config['schedulers']['calendars']['calendar']]



	print "Configuration preparsing finished. Found:"
	print ""
	print len(conf_devices), " devices"
	print len(conf_devices_streetlight), " streetlight devices"
	print len(conf_devices_controller), " controller devices"
	print len(conf_devices_other), " other devices"
	print len(conf_global_params), " global parameters to apply to all devices"
	print len(conf_resources), " resources"
	print len(conf_programs), " programs"
	print len(conf_calendars), " calendars"


	# This is a processing part
	#if controller is not defined define it first
	if dev_mode is 'COMPLETE':
		# Deal with controller
		resp = process_controller(conf_devices_controller[0], 'COMPLETE', conf_params)
		if resp is not 'OK':
			errors.append(resp)
			return errors
		
		# Deal with streetlights
		db.session.delete(models.Streetlight.query.all())
		for dev in conf_devices_streetlight:
			resp = process_streetlight(conf_devices_streetlight, 'COMPLETE', conf_params)
			if resp is not 'OK':
				errors.append(resp)
		
		# Deal with other devices
		for dev in conf_devices_other:
			errors.append('Error: This type of device is not supported yet')
			

	elif dev_mode is 'COMPLETE_BUT_CONTROLLER':
		# Deal with streetlights
		db.session.delete(models.Streetlight.query.all())
		for dev in conf_devices_streetlight:
			resp = process_streetlight(conf_devices_streetlight, 'COMPLETE', conf_params)
			if resp is not 'OK':
				errors.append(resp)
		
		# Deal with other devices
		for dev in conf_devices_other:
			errors.append('Error: This type of device is not supported yet')
	
	elif dev_mode is 'CONTROLLER_ONLY':
		# Deal with controller
		resp = process_controller(conf_devices_controller[0], 'UPDATE', conf_params)
		if resp is not 'OK':
			errors.append(resp)
			return errors

	elif dev_mode is 'UPDATE_BUT_CONTROLLER':
		# Deal with streetlights
		for dev in conf_devices_streetlight:
			resp = process_streetlight(conf_devices_streetlight, 'UPDATE', conf_params)
			if resp is not 'OK':
				errors.append(resp)
		
		# Deal with other devices
		for dev in conf_devices_other:
			errors.append('Error: This type of device is not supported yet')

	elif dev_mode is 'UPDATE':
		# Deal with controller
		resp = process_controller(conf_devices_controller[0], 'UPDATE', conf_params)
		if resp is not 'OK':
			errors.append(resp)
		
		# Deal with streetlights
		for dev in conf_devices_streetlight:
			resp = process_streetlight(conf_devices_streetlight, 'UPDATE', conf_params)
			if resp is not 'OK':
				errers.append(resp)
		
		# Deal with other devices
		for dev in conf_devices_other:
			errors.append('Error: This type of device is not supported yet')
	
	return errors
		

def process_set_command(command):
	""" Processes a set control command
	:param command: individual or group set command
	:returns: response dictionary
	"""
	response = {}
	dev_id = ''
	dev_group_id=''
	error = ''

	# reading the command	
	if '@id' in command.keys():
		dev_id = command['@id']
	elif '@dimmingGroupName' in command.keys():
		dev_group_name = command['@dimmingGroupName']
	dev_ctrlId = command['@ctrlId']
	# dev_networkId = command['@networkId']
	comm_meaning = command['@meaning']
	comm_value = command['#text']
	
	# if individual device command
	if dev_id != '':
		streetlight = db.session.query(Streetlight).filter(Streetlight.controllerStrId==dev_ctrlId).filter(Streetlight.idOnController==dev_id)
		if len(streetlight) == 0:
			error = 'Error: No devices found with this id'
		elif len(streetlight) > 1:
			error = 'Error: Too many streetlights found with this id'
		else:
			try:
				streetlight[0].comm_meaning = comm_value
			except:
				error = 'Error: Failed setting ', comm_meaning, ' to this device' 
		
	# if a dimming group command
	elif dev_group_name:
		streetlight = db.session.query(Streetlight).filter(Streetlight.cdimmingGroupName==dev_group_name)
		if len(streetlight) == 0:
			error = 'Error: No devices found for this dimming group'
		else:
			for sl in streetlight:
				try:
					sl.comm_meaning = comm_value
				except:
					error = 'Error: Failed setting ', comm_meaning, ' to this group'

	if error == '':
		db.session.commit()
		response['status'] = 'OK'
		response['DATE'] = time.strftime("%Y-%m-%d %H:%M:%S")
		response['error'] = []
	else:
		db.session.rollback()
		response['status'] = 'ERROR'
		response['DATE'] = time.strftime("%Y-%m-%d %H:%M:%S")
		response['error'] = error

	return response

def process_get_command(command):
	""" Processes a get control command
	:param command: individual get command
	:returns: response dictionary
	"""
	response = {}
	dev_id = ''
	error = ''
	value = []

	# reading the command	
	dev_id = command['@id']
	dev_ctrlId = command['@ctrlId']
	# dev_networkId = command['@networkId']
	comm_meaning = command['@meaning']
	
	# if individual device command
	streetlight = db.session.query(Streetlight).filter(Streetlight.controllerStrId==dev_ctrlId).filter(Streetlight.idOnController==dev_id)
	if len(streetlight) == 0:
		error = 'Error: No devices found with this id'
	elif len(streetlight) > 1:
		error = 'Error: Too many streetlights found with this id'
	else:
		try:
			value = streetlight[0].comm_meaning
		except:
			error = 'Error: Failed setting ', comm_meaning, ' to this device' 

	if error == '':
		response['status'] = 'OK'
		response['DATE'] = time.strftime("%Y-%m-%d %H:%M:%S")
		response['value'] = value
		response['error'] = []
	else:
		response['status'] = 'ERROR'
		response['DATE'] = time.strftime("%Y-%m-%d %H:%M:%S")
		response['value'] = value
		response['error'] = error

	return response	

def parse_commands(payload):
	""" Parses a control command and set devices
	:param payload: control dictionary structure
	:returns: response dictionary to be converted to XML in the caller function
	"""
	
	commands = payload['commands']
	
	full_response = {}
	full_response['responses'] = {}
	full_response['responses']['response'] = []
	
	error = ''

	# Check if one controller is defined in the system
	db_controllers = models.Controller.query.all()
	# The controller is defined in the system
	if len(db_controllers)==1:
		print "One controller is defined in the system"
		ctrl_defined = True
		controller = db_controllers[0]
		# Wrong ctrlId
		if controller.controllerStrId != ctrlId:
			error = "Error: configuration ctrlId doesn't match this controller controllerStrId" 
			print error	
	elif len(db_controllers)>1:
		error = "Error: to many controllers are defined in the system" 
		print error

	if error != '':
		response['status'] = 'ERROR'
		response['DATE'] = time.strftime("%Y-%m-%d %H:%M:%S")
		response['error'] = error
		full_response['responses']['response'].append(response)
		return full_response
		
	
	# Checking command structure

	comm_set = []	
	comm_set_group = []
	comm_set_device = []
	comm_get = []

	# Checking set commands
	if 'set' in commands.keys():
		
		if type(commands['set']) is list:
			comm_set = commands['set']
		else:
			comm_set = [commands['set']]
		
		for comm in comm_set:
			if '@id' in comm.keys():
				comm_set_device.append(comm)
			elif '@dimmingGroupName' in comm.keys():
				comm_set_group.append(comm)

	# Checking get commands
	if 'get' in commands.keys():
		
		if type(commands['get']) is list:
			comm_get = commands['get']
		else:
			comm_get = [commands['get']]

	print "Commands preparsing finished. Found:"
	print ""
	print len(comm_get), " Get commands"
	print len(comm_set), " Set commands. Of them:"
	print len(comm_set_device), " Individual device set commands"
	print len(comm_set_group), " Group set commands"





	# Processing set group commands
	for comm in comm_set_group:
		resp_dict = process_set_command(comm)
		full_response['responses']['response'].append(resp_dict)

	# Processing set individual commands
	for comm in comm_set_device:
		resp_dict = process_set_command(comm)
		full_response['responses']['response'].append(resp_dict)

	# Processing get commands
	for comm in comm_set_group:
		resp_dict = process_get_command(comm)
		full_response['responses']['response'].append(resp_dict)

	return full_response

		

@app.route('/', methods=['POST'])
def process_request():
	""" Main configuration and control function. Processes either a configuration or a commands payload from SLV to Gateway
	:returns: "OK" or error XML structure
	"""

	if not request.data:
		# Send an error response if no XML recieved
        	abort(400)
	
	#command_XML1 = BeautifulSoup(request.data, 'xml')
	#print(command_XML1.prettify())	
	
	# Parse XML command to dictionary
	try:
		command_XML = xmltodict.parse(request.data)
	except:
		# if failed to parse XML send an error response
		abort(400)		

	if 'configuration' in command_XML.keys():
		print "executing configuration"
		response = parse_configuration(command_XML)
		return response

	elif 'commands' in command_XML.keys():
		print "executing commands"
		response = parse_commands(command_XML)
		return "command_response"

	else:
		# if wrong root in parsed XML return an error
		print "bad_request_response 2"
		return "bad_request_response" 




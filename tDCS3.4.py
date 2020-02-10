# necessary imports
import sys
import time
from PyQt5 import QtGui
from PyQt5 import QtCore
from PyQt5 import QtWidgets


class Helper():
	def __init__(self):
		# initialize instance variables
		self.allowExit = True
		self.index = 1
		self.PAIN_THRESHOLD = 7
		self.FIRST_SESSION = self.isFirstSession()

		# email
		self.recipients = ['CharvetKruppResearch@nyulangone.org', 'Michael.Shaw@nyulangone.org']
		self.NUM_DEFAULT_EMAILS = len(self.recipients)

		# width and height of the screen
		self.WIDTH = QtWidgets.QDesktopWidget().width()
		self.HEIGHT = QtWidgets.QDesktopWidget().height()

		# holds various layouts in this window
		self.stacked_layout = QtWidgets.QStackedLayout()

		# dictionary to hold user data
		self.values = {}
		self.summaryValues = {}

	def addActionToolBar(self):
		helpAct = QtWidgets.QAction(QtGui.QIcon('data/images/help.png'), 'Help', self)
		helpAct.setShortcut('Ctrl+H')
		helpAct.triggered.connect(lambda:self.help(self.studyID))

		changeVoiceAct = QtWidgets.QAction(QtGui.QIcon('data/images/voice.jpg'), 'Change voice', self)
		changeVoiceAct.setShortcut('Ctrl+V')
		changeVoiceAct.triggered.connect(self.changeVoice)

		self.muteAct = QtWidgets.QAction(QtGui.QIcon('data/images/mute.jpg'), 'Unmute', self)
		self.muteAct.setShortcut('Ctrl+M')
		self.muteAct.triggered.connect(self.changeMuteStatus)

		self.unmuteAct = QtWidgets.QAction(QtGui.QIcon('data/images/unmute.jpg'), 'Mute', self)
		self.unmuteAct.setShortcut('Ctrl+M')
		self.unmuteAct.triggered.connect(self.changeMuteStatus)

		self.toolbar = self.addToolBar('Actions')
		self.toolbar.setMovable(False)
		self.toolbar.addAction(helpAct)
		self.toolbar.addAction(changeVoiceAct)
		self.toolbar.addAction(self.unmuteAct)

	def changeVoice(self):
		choice = QtWidgets.QMessageBox.question(self, 'Confirmation', 'Are you sure you want to change the voice?',
			QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.Yes)
		if choice == QtWidgets.QMessageBox.Yes:
			# change the voice
			if self.audioPath and self.audioPath == 'data/sound/voice1/':
				self.audioPath = 'data/sound/voice2/'
			else:
				self.audioPath = 'data/sound/voice1/'
			# change the current audio file
			if self.audioFile:
				audioFileSplit = self.audioFile.rsplit('/', 1)
				audioFile = audioFileSplit[1]
				self.audioFile = self.audioPath + audioFile

	def addWindowOnTopFlag(self):
		# application window will stay on top
		self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
		self.show()

	def removeWindowOnTopFlag(self):
		# allow user to minimize application window
		self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowStaysOnTopHint)
		self.show()

	def isFirstSession(self):
		try:
			self.user_data = pd.read_csv('data/user/feedback.csv')
			return False
		except FileNotFoundError:
			return True

	def gotoPreviousWidget(self):
		global ongoingSpeech
		if not ongoingSpeech:
			self.stacked_layout.removeWidget(self.stacked_layout.currentWidget())  # remove this from the stacked layout
			self.index -= 1
			self.stacked_layout.setCurrentIndex(self.index)  # change the visible layout in the stack

	def setFontStyle(self, label, size=20, color='white', alignment=QtCore.Qt.AlignCenter):
		label.setWordWrap(True)
		label.setFont(QtGui.QFont('Calibri', size))
		label.setStyleSheet('color: ' + color + ';')
		label.setAlignment(alignment)

	def setRadioButtonStyle(self, radioButton):
		radioButton.setFont(QtGui.QFont('Calibri', 15))
		radioButton.setStyleSheet('color: white;')

	def setRadioButtonLayoutStyle(self, radioButtonLayout):
		radioButtonLayout.setContentsMargins(self.WIDTH * 0.01, self.HEIGHT * 0, self.WIDTH * 0.01, self.HEIGHT * 0)

	def setCheckBoxStyle(self, checkBox, selected=False):
		checkBox.setFont(QtGui.QFont('Calibri', 14))
		checkBox.setFixedWidth(self.WIDTH * 0.25)
		checkBox.setFixedHeight(self.HEIGHT * 0.03)
		if selected:
			checkBox.setStyleSheet('color: yellow;')
		else:
			checkBox.setStyleSheet('color: white;')

	def setLineEditStyle(self, lineEdit, widthFactor=0.15, heightFactor=0.04):
		lineEdit.setFont(QtGui.QFont('Calibri', 12))
		lineEdit.setFixedWidth(self.WIDTH * widthFactor)
		lineEdit.setFixedHeight(self.HEIGHT * heightFactor)

	def setPlainTextEditStyle(self, plainTextEdit):
		plainTextEdit.setFont(QtGui.QFont('Calibri', 12))

	def setButtonStyle(self, button):
		button.setFont(QtGui.QFont('Calibri', 13))
		button.setFixedHeight(self.HEIGHT * 0.05)
		button.setAutoDefault(True)  # makes the button clickable by enter or return key

	def setComboBoxStyle(self, comboBox, widthFactor=0.15, heightFactor=0.04):
		comboBox.setFont(QtGui.QFont('Calibri', 12))
		comboBox.setStyleSheet('combobox-popup:0;')
		comboBox.setFixedWidth(self.WIDTH * widthFactor)
		comboBox.setFixedHeight(self.HEIGHT * heightFactor)

	def setSpinBoxStyle(self, spinBox):
		spinBox.setFont(QtGui.QFont('Calibri', 12))
		spinBox.setFixedWidth(self.WIDTH * 0.04)
		spinBox.setFixedHeight(self.HEIGHT * 0.04)

	def setProgressBarStyle(self, progressBar):
		progressBar.setFont(QtGui.QFont('Calibri', 12))
		progressBar.setFixedHeight(self.HEIGHT * 0.04)

	def setTableStyle(self, table):
		table.setAlternatingRowColors(True)
		table.setStyleSheet('alternate-background-color: gray;')

	def setTableRowBackgroundColor(self, table, rowIndex, hexColorCode):
		for colIndex in range(table.columnCount()):
			table.setItem(rowIndex, colIndex, QtWidgets.QTableWidgetItem())
			table.item(rowIndex, colIndex).setBackground(QtGui.QColor(hexColorCode))

	def setVisualAnalogScaleSpacing(self, layout):
		layout.setStretch(0, 0)
		layout.setContentsMargins(self.WIDTH * 0, self.HEIGHT * 0, self.WIDTH * 0, self.HEIGHT * 0.25)

	def createTextDialog(self, title, label, echoMode=None, option=None):
		inputDialog = QtWidgets.QInputDialog()
		inputDialog.setInputMode(QtWidgets.QInputDialog.TextInput)
		if option: inputDialog.setOption(option)
		if echoMode: inputDialog.setTextEchoMode(echoMode)
		inputDialog.setWindowTitle(title)
		inputDialog.setLabelText(label)
		inputDialog.setWindowIcon(QtGui.QIcon('data/images/logo.ico'))
		inputDialog.setFont(QtGui.QFont('Calibri', 13))
		return inputDialog, inputDialog.exec_()

	def createDoubleDialog(self, title, label, value, minimum, decimals):
		inputDialog = QtWidgets.QInputDialog()
		inputDialog.setInputMode(QtWidgets.QInputDialog.DoubleInput)
		inputDialog.setDoubleValue(value)
		inputDialog.setDoubleMinimum(minimum)
		inputDialog.setDoubleDecimals(decimals)
		inputDialog.setWindowTitle(title)
		inputDialog.setLabelText(label)
		inputDialog.setWindowIcon(QtGui.QIcon('data/images/logo.ico'))
		inputDialog.setFont(QtGui.QFont('Calibri', 13))
		return inputDialog, inputDialog.exec_()

	def checkBattery(self):
		battery = psutil.sensors_battery()
		try:
			plugged = battery.power_plugged
			battery_sufficient = False if battery.percent < self.minBatteryRequired else True
		except AttributeError:
			# machine is a desktop
			battery_sufficient, plugged = True, True
		return battery_sufficient, plugged

	def isValidPortalInfo(self):
		subjectDetails = ['Master ID', 'Subject study', 'Subject tDCS dose', 'Subject tDCS dose duration', 'Subject training regimen', 'Subject baseline examination']
		for subjectDetail in subjectDetails:
			if subjectDetail not in self.values or self.values[subjectDetail] == '':
				return False
		return True

	def help(self, studyID=None):
		if not studyID:
			studyID = self.lineEdit_studyID.text().strip().replace(' ','')
			if studyID == '':
				studyID, ok = QtWidgets.QInputDialog.getText(self, 'Study ID', 'Please enter your study ID:')
				if not ok:
					return
		choice = QtWidgets.QMessageBox.question(self, 'Confirmation', 'Are you sure you want to email NYU MS Center?',
			QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.Yes)
		if choice == QtWidgets.QMessageBox.Yes:
			subject = 'tDCS ALERT: Study ID {} !!'.format(studyID)
			body = 'A patient with study ID \'{}\' needs your help.'.format(studyID)
			success = self.sendEmail(subject, body)
			if success:
				QtWidgets.QMessageBox.information(self, 'Success',
					'We have received your email and will call you shortly. You can also reach out to us at (929) 455-5088.',
					QtWidgets.QMessageBox.Ok)
			else:
				QtWidgets.QMessageBox.critical(self, 'Failed',
					'We could not receive your email. Please reach out directly to us at (929) 455-5088.',
					QtWidgets.QMessageBox.Ok)

	def highPain(self, studyID):
		subject = 'tDCS ALERT: Study ID {} !!'.format(studyID)
		body = 'A patient with study ID \'{}\' is in high pain.'.format(studyID)
		success = self.sendEmail(subject, body)
		# if success:
		# 	QtWidgets.QMessageBox.information(self, 'Success',
		# 		'We noticed that you are in high pain and will call you shortly. You can also reach out to us at (929) 455-5088. This session will now end.',
		# 		QtWidgets.QMessageBox.Ok)
		# else:
		# 	QtWidgets.QMessageBox.critical(self, 'Failed',
		# 		'We noticed that you are in high pain but an email could not be sent from your computer. Please reach out directly to us at (929) 455-5088. This session will now end.',
		# 		QtWidgets.QMessageBox.Ok)
		# self.saveUserData()
		# self.sendUserData(studyID)
		# sys.exit()

	def sendEmail(self, subject, content, files=None):

		user = 'Research.tDCS@gmail.com'
		password = '204319#scdT@M13&19S'

		SERVER = 'smtp.gmail.com'
		PORT = 465

		FROM = user
		TO = self.recipients if type(self.recipients) is list else [self.recipients]
		SUBJECT = subject
		TEXT = content

		# message = """From: %s\nTo: %s\nSubject: %s\n\n%s
		# """ % (FROM, ', '.join(TO), SUBJECT, TEXT)

		message = MIMEMultipart()
		message['From'] = user
		message['To'] = ', '.join(TO)
		message['Subject'] = SUBJECT

		# email content
		body = """<html>
					<body>
					%s
					</body>
				  </html>
			   """ % (TEXT)

		message.attach(MIMEText(body, 'html'))

		if files:
			for attach_file in files:
				attachment = open(attach_file, 'rb')
				file_name = os.path.basename(attach_file)
				part = MIMEBase('application','octet-stream')
				part.set_payload(attachment.read())
				part.add_header('Content-Disposition', 'attachment', filename=file_name)
				encoders.encode_base64(part)
				message.attach(part)

		try:
			SERVER_SSL = smtplib.SMTP_SSL()
			SERVER_SSL.connect(SERVER, PORT)
			SERVER_SSL.ehlo()
			SERVER_SSL.login(user, password)
			SERVER_SSL.sendmail(FROM, TO, message.as_string())
			SERVER_SSL.quit()
			SERVER_SSL.close()
			return True
		except Exception as e:
			print(e)
			return False

	def recordRadioButtonSelection(self, radioButtonList, label):
		for radioButton in radioButtonList:
			if radioButton.isChecked():
				intensity = int(radioButton.text())
				self.values[label] = intensity
				radioButton.setStyleSheet('color: red;')
			else:
				radioButton.setStyleSheet('color: white;')

	def preSessionSideEffectIntensity(self, checkBox, preSideEffects):
		if checkBox.isChecked():
			self.setCheckBoxStyle(checkBox, selected=True)
			self.removeWindowOnTopFlag()
			dialog = CustomDialog(title='{}'.format(preSideEffects[checkBox]),
								  labelText='How intense was the side effect?')
			if dialog.exec_():
				self.values['Intensity: Pre-Session ' + preSideEffects[checkBox]] = dialog.getIntensityLevel()
				self.removeWindowOnTopFlag()
				inputDialog, ok = self.createDoubleDialog(title='{}'.format(preSideEffects[checkBox]),
					label='How long did the side effect last? (in minutes)', value=1, minimum=0, decimals=1)
				duration = inputDialog.doubleValue()
				if ok:
					self.values['Duration: Pre-Session ' + preSideEffects[checkBox]] = duration
				else:
					checkBox.setChecked(False)
				self.addWindowOnTopFlag()
			else:
				checkBox.setChecked(False)
			self.addWindowOnTopFlag()
		else:
			self.setCheckBoxStyle(checkBox)
			self.values['Intensity: Pre-Session ' + preSideEffects[checkBox]] = 0
			self.values['Duration: Pre-Session ' + preSideEffects[checkBox]] = 0

	def preSessionOtherSideEffectIntensity(self, checkBox, preOtherSideEffects):
		if checkBox.isChecked():
			self.setCheckBoxStyle(checkBox, selected=True)
			moreSideEffects = True
			while moreSideEffects:
				self.removeWindowOnTopFlag()
				inputDialog, ok = self.createTextDialog(title='Other', option=QtWidgets.QInputDialog.UsePlainTextEditForTextInput,
					label='Please describe the other side effect that you experienced after your last treatment session ended.')
				otherSideEffect = inputDialog.textValue().strip()

				if ok and otherSideEffect != '':
					self.removeWindowOnTopFlag()
					dialog = CustomDialog(title='{}'.format(otherSideEffect),
										  labelText='How intense was the side effect?')
					if dialog.exec_():
						intensity_level = dialog.getIntensityLevel()
						self.values['Intensity: Pre-Session Other'].append((otherSideEffect, intensity_level))
						self.removeWindowOnTopFlag()
						inputDialog, ok = self.createDoubleDialog(title='{}'.format(otherSideEffect),
							label='How long did the side effect last? (in minutes)', value=1, minimum=0, decimals=1)
						duration = inputDialog.doubleValue()
						if ok:
							self.values['Duration: Pre-Session Other'].append((otherSideEffect, duration))
							currentText = preOtherSideEffects.text()
							newText = currentText + '\n' + str(otherSideEffect) + '\n' + 'Intensity: ' + str(intensity_level) + ' out of 10' + '\n' + 'Duration: ' + str(duration) + ' minutes \n'
							preOtherSideEffects.setText(newText)
							self.setFontStyle(preOtherSideEffects, size=12, alignment=QtCore.Qt.AlignLeft)
							preOtherSideEffects.adjustSize()
							choice = QtWidgets.QMessageBox.question(self, 'Other Side Effect',
								'Did you feel any other side effect or sensation during the stimulation?', QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.Yes)
							if choice == QtWidgets.QMessageBox.Yes:
								moreSideEffects = True
							else:
								moreSideEffects = False
						else:
							if preOtherSideEffects.text() == '':
								checkBox.setChecked(False)
							moreSideEffects = False
						self.addWindowOnTopFlag()
					else:
						if preOtherSideEffects.text() == '':
							checkBox.setChecked(False)
						moreSideEffects = False
					self.addWindowOnTopFlag()
				else:
					if preOtherSideEffects.text() == '':
						checkBox.setChecked(False)
					moreSideEffects = False
				self.addWindowOnTopFlag()
		else:
			self.setCheckBoxStyle(checkBox)
			self.values['Intensity: Pre-Session Other'] = []
			self.values['Duration: Pre-Session Other'] = []
			preOtherSideEffects.setText('')
			preOtherSideEffects.adjustSize()

	def postSessionSideEffectIntensity(self, checkBox, postSideEffects):
		if checkBox.isChecked():
			self.setCheckBoxStyle(checkBox, selected=True)
			self.removeWindowOnTopFlag()
			dialog = CustomDialog(title='{}'.format(postSideEffects[checkBox]),
								  labelText='How intense was the side effect?')
			if dialog.exec_():
				self.values['Intensity: Post-Session ' + postSideEffects[checkBox]] = dialog.getIntensityLevel()
				self.removeWindowOnTopFlag()
				inputDialog, ok = self.createDoubleDialog(title='{}'.format(postSideEffects[checkBox]),
					label='How long did the side effect last? (in minutes)', value=1, minimum=0, decimals=1)
				duration = inputDialog.doubleValue()
				if ok:
					self.values['Duration: Post-Session ' + postSideEffects[checkBox]] = duration
				else:
					checkBox.setChecked(False)
				self.addWindowOnTopFlag()
			else:
				checkBox.setChecked(False)
			self.addWindowOnTopFlag()
		else:
			self.setCheckBoxStyle(checkBox)
			self.values['Intensity: Post-Session ' + postSideEffects[checkBox]] = 0
			self.values['Duration: Post-Session ' + postSideEffects[checkBox]] = 0

	def postSessionOtherSideEffectIntensity(self, checkBox, postOtherSideEffects):
		if checkBox.isChecked():
			self.setCheckBoxStyle(checkBox, selected=True)
			moreSideEffects = True
			while moreSideEffects:
				self.removeWindowOnTopFlag()
				inputDialog, ok = self.createTextDialog(title='Other', option=QtWidgets.QInputDialog.UsePlainTextEditForTextInput,
					label='Please describe the other side effect that you experienced during the stimulation.')
				otherSideEffect = inputDialog.textValue().strip()

				if ok and otherSideEffect != '':
					self.removeWindowOnTopFlag()
					dialog = CustomDialog(title='{}'.format(otherSideEffect),
										  labelText='How intense was the side effect?')
					if dialog.exec_():
						intensity_level = dialog.getIntensityLevel()
						self.values['Intensity: Post-Session Other'].append((otherSideEffect, intensity_level))
						self.removeWindowOnTopFlag()
						inputDialog, ok = self.createDoubleDialog(title='{}'.format(otherSideEffect),
							label='How long did the side effect last? (in minutes)', value=1, minimum=0, decimals=1)
						duration = inputDialog.doubleValue()
						if ok:
							self.values['Duration: Post-Session Other'].append((otherSideEffect, duration))
							currentText = postOtherSideEffects.text()
							newText = currentText + '\n' + str(otherSideEffect) + '\n' + 'Intensity: ' + str(intensity_level) + ' out of 10' + '\n' + 'Duration: ' + str(duration) + ' minutes \n'
							postOtherSideEffects.setText(newText)
							self.setFontStyle(postOtherSideEffects, size=12, alignment=QtCore.Qt.AlignLeft)
							postOtherSideEffects.adjustSize()
							choice = QtWidgets.QMessageBox.question(self, 'Other Side Effect',
								'Did you feel any other side effect or sensation during the stimulation?', QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.Yes)
							if choice == QtWidgets.QMessageBox.Yes:
								moreSideEffects = True
							else:
								moreSideEffects = False
						else:
							if postOtherSideEffects == '':
								checkBox.setChecked(False)
							moreSideEffects = False
						self.addWindowOnTopFlag()
					else:
						if postOtherSideEffects == '':
							checkBox.setChecked(False)
						moreSideEffects = False
					self.addWindowOnTopFlag()
				else:
					if postOtherSideEffects == '':
						checkBox.setChecked(False)
					moreSideEffects = False
				self.addWindowOnTopFlag()
		else:
			self.setCheckBoxStyle(checkBox)
			self.values['Intensity: Post-Session Other'] = []
			self.values['Duration: Post-Session Other'] = []
			postOtherSideEffects.setText('')
			postOtherSideEffects.adjustSize()

	def saveUserData(self):
		if self.index > 2:
			if self.FIRST_SESSION:
				self.user_data = pd.DataFrame()
				if 'Session number' not in self.values or self.values['Session number'] == '':
					self.values['Session number'] = 1
			else:
				if 'Master ID' not in self.values:
					self.values['Master ID'] = self.user_data['Master ID'].iloc[-1]
					self.values['Subject study'] = self.user_data['Subject study'].iloc[-1]
					self.values['Subject tDCS dose'] = self.user_data['Subject tDCS dose'].iloc[-1]
					self.values['Subject tDCS dose duration'] = str(self.user_data['Subject tDCS dose duration'].iloc[-1])
					self.values['Subject training regimen'] = self.user_data['Subject training regimen'].iloc[-1]
					self.values['Subject baseline examination'] = self.user_data['Subject baseline examination'].iloc[-1]

			cols = [
				'Master ID', 'Study ID', 'Subject study', 'Session number', 'Subject tDCS dose', 'Subject tDCS dose duration', 'Subject training regimen',
				'Date', 'Start time', 'End time', 'Study technician', 'Dose code', 'Subject baseline examination',
				'Pre-Session Headset Device Pain', 'Pre-Session MS pain', 'Pre-Session Fatigue', 'Pre-Session Headset-Related Side Effects',
				'Intensity: Pre-Session Skin tingling', 'Duration: Pre-Session Skin tingling',
				'Intensity: Pre-Session Skin itching', 'Duration: Pre-Session Skin itching',
				'Intensity: Pre-Session Sensations of warmth', 'Duration: Pre-Session Sensations of warmth',
				'Intensity: Pre-Session Other', 'Duration: Pre-Session Other', 'Pre-Session Other Side Effects Text',
				'Hours slept', 'Wake up time', 'Time since woke up', 'Sleep quality', 'Contact quality',
				'Pre-Session PANAS: Interested', 'Pre-Session PANAS: Distressed', 'Pre-Session PANAS: Excited', 'Pre-Session PANAS: Upset',
				'Pre-Session PANAS: Strong', 'Pre-Session PANAS: Guilty', 'Pre-Session PANAS: Scared', 'Pre-Session PANAS: Hostile',
				'Pre-Session PANAS: Enthusiastic', 'Pre-Session PANAS: Proud', 'Pre-Session PANAS: Irritable', 'Pre-Session PANAS: Alert',
				'Pre-Session PANAS: Ashamed', 'Pre-Session PANAS: Inspired', 'Pre-Session PANAS: Nervous', 'Pre-Session PANAS: Determined',
				'Pre-Session PANAS: Attentive', 'Pre-Session PANAS: Jittery', 'Pre-Session PANAS: Active', 'Pre-Session PANAS: Afraid',
				'Ongoing-Session Headset Device Pain',
				'Post-Session Headset Device Pain', 'Post-Session MS pain', 'Post-Session Fatigue', 'Post-Session Headset-Related Side Effects',
				'Intensity: Post-Session Skin tingling', 'Duration: Post-Session Skin tingling',
				'Intensity: Post-Session Skin itching', 'Duration: Post-Session Skin itching',
				'Intensity: Post-Session Sensations of warmth', 'Duration: Post-Session Sensations of warmth',
				'Intensity: Post-Session Other', 'Duration: Post-Session Other', 'Post-Session Other Side Effects Text',
				'Post-Session PANAS: Interested', 'Post-Session PANAS: Distressed', 'Post-Session PANAS: Excited', 'Post-Session PANAS: Upset',
				'Post-Session PANAS: Strong', 'Post-Session PANAS: Guilty', 'Post-Session PANAS: Scared', 'Post-Session PANAS: Hostile',
				'Post-Session PANAS: Enthusiastic', 'Post-Session PANAS: Proud', 'Post-Session PANAS: Irritable', 'Post-Session PANAS: Alert',
				'Post-Session PANAS: Ashamed', 'Post-Session PANAS: Inspired', 'Post-Session PANAS: Nervous', 'Post-Session PANAS: Determined',
				'Post-Session PANAS: Attentive', 'Post-Session PANAS: Jittery', 'Post-Session PANAS: Active', 'Post-Session PANAS: Afraid',
				'Technical Problems'
			]

			self.user_data = self.user_data.append(self.values, ignore_index=True)
			try:
				self.user_data.to_csv('data/user/feedback.csv', index=False, columns=cols)
			except PermissionError:
				choice = QtWidgets.QMessageBox.critical(self, 'Close file',
					'Please close the feedback file to continue.', QtWidgets.QMessageBox.Retry)
				if choice == QtWidgets.QMessageBox.Retry:
					self.saveUserData()

			self.saveUserSummaryData()

	def saveUserSummaryData(self):
		try:
			self.summary_user_data = pd.read_csv('data/user/feedback_summary.csv')
		except FileNotFoundError:
			self.summary_user_data = pd.DataFrame()

		labels = [
			'Master ID', 'Study ID', 'Subject study', 'Session number', 'Subject tDCS dose',
			'Subject tDCS dose duration', 'Subject training regimen', 'Date', 'Start time',
			'Subject baseline examination', 'Hours slept', 'Wake up time', 'Time since woke up',
			'Sleep quality', 'Contact quality', 'Pre-Session Headset Device Pain',
			'Ongoing-Session Headset Device Pain', 'Post-Session Headset Device Pain'
		]

		for label in labels:
			if label in self.values:
				self.summaryValues[label] = self.values[label]

		if 'Post-Session MS pain' in self.values and 'Pre-Session MS pain' in self.values:
			self.summaryValues['Change: MS pain'] = self.values['Post-Session MS pain'] - self.values['Pre-Session MS pain']
		if 'Post-Session Fatigue' in self.values and 'Pre-Session Fatigue' in self.values:
			self.summaryValues['Change: Fatigue'] = self.values['Post-Session Fatigue'] - self.values['Pre-Session Fatigue']

		measures = ['Intensity: ', 'Duration: ']
		sessionPrePost = ['Pre-Session ', 'Post-Session ']
		labels = ['Skin tingling', 'Skin itching', 'Sensations of warmth', 'Other']

		for prepost in sessionPrePost:
			self.summaryValues[prepost + 'Side Effects'] = 'No'
			for measure in measures:
				for label in labels:
					if label == 'Other':
						if measure + prepost + label in self.values and len(self.values[measure + prepost + label]) > 0:
							self.summaryValues[prepost + 'Side Effects'] = 'Yes'
							break
					elif measure + prepost + label in self.values and self.values[measure + prepost + label] > 0:
						self.summaryValues[prepost + 'Side Effects'] = 'Yes'
						break

		sessionPrePost = ['Pre-Session PANAS: ', 'Post-Session PANAS: ']
		labels = [
			'Interested', 'Distressed', 'Excited', 'Upset', 'Strong', 'Guilty', 'Scared',
			'Hostile', 'Enthusiastic', 'Proud', 'Irritable', 'Alert', 'Ashamed', 'Inspired',
			'Nervous', 'Determined', 'Attentive', 'Jittery', 'Active', 'Afraid'
		]

		for prepost in sessionPrePost:
			self.summaryValues[prepost + 'Positive affect score'] = 0
			self.summaryValues[prepost + 'Negative affect score'] = 0
			for i, label in enumerate(labels):
				if prepost + label in self.values:
					if i % 2 == 0:
						self.summaryValues[prepost + 'Positive affect score'] += self.values[prepost + label]
					else:
						self.summaryValues[prepost + 'Negative affect score'] += self.values[prepost + label]

		self.summaryValues['Change: PANAS Positive affect score'] = self.summaryValues['Post-Session PANAS: Positive affect score'] - self.summaryValues['Pre-Session PANAS: Positive affect score']
		self.summaryValues['Change: PANAS Negative affect score'] = self.summaryValues['Post-Session PANAS: Negative affect score'] - self.summaryValues['Pre-Session PANAS: Negative affect score']

		cols = [
			'Master ID', 'Study ID', 'Subject study', 'Session number', 'Subject tDCS dose',
			'Subject tDCS dose duration', 'Subject training regimen', 'Date', 'Start time',
			'Subject baseline examination', 'Hours slept', 'Wake up time', 'Time since woke up',
			'Sleep quality', 'Contact quality', 'Change: MS pain', 'Change: Fatigue',
			'Pre-Session Side Effects', 'Post-Session Side Effects', 'Pre-Session Headset Device Pain',
			'Ongoing-Session Headset Device Pain', 'Post-Session Headset Device Pain',
			'Pre-Session PANAS: Positive affect score', 'Pre-Session PANAS: Negative affect score',
			'Post-Session PANAS: Positive affect score', 'Post-Session PANAS: Negative affect score',
			'Change: PANAS Positive affect score', 'Change: PANAS Negative affect score'
		]

		self.summary_user_data = self.summary_user_data.append(self.summaryValues, ignore_index=True)
		try:
			self.summary_user_data.to_csv('data/user/feedback_summary.csv', index=False, columns=cols)
		except PermissionError:
			choice = QtWidgets.QMessageBox.critical(self, 'Close file',
				'Please close the feedback_summary file to continue.', QtWidgets.QMessageBox.Retry)
			if choice == QtWidgets.QMessageBox.Retry:
				self.saveUserSummaryData()

		self.dataSaved = True

	def sendUserData(self, studyID):
		if self.index > 2:
			self.allowExit = False
			retries = 3
			subject = 'tDCS data for Study ID {}'.format(studyID)
			body = 'Please find attached the csv file containing data of patient with study ID \'{}\'.'.format(studyID)
			feedback = os.getcwd() + '\\data\\user\\feedback.csv'
			feedbackSummary = os.getcwd() + '\\data\\user\\feedback_summary.csv'
			files = [feedback, feedbackSummary]
			while not self.sendEmail(subject, body, files) and retries > 0:
				retries -= 1
			if retries > 0:
				self.dataSent = True
			self.allowExit = True

	def exitApplication(self, studyID=None):
		global ongoingSpeech
		if not ongoingSpeech and self.allowExit:
			if not studyID:
				sys.exit()
			choice = QtWidgets.QMessageBox.question(self, 'Confirmation', 'Are you sure you want to exit tDCS?',
				QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)
			if choice == QtWidgets.QMessageBox.Yes:
				if not self.dataSaved:
					self.saveUserData()
				if not self.dataSent:
					self.sendUserData(studyID)
				sys.exit()


class PlayAudio(QtCore.QThread):
	def __init__(self, audioFile, restore, buttonsToDisable=[]):
		QtCore.QThread.__init__(self)
		self.audioFile = audioFile
		self.restore = restore
		self.buttonsToDisable = buttonsToDisable

	def run(self):
		global ongoingSpeech
		ongoingSpeech = True
		for buttonToDisable in self.buttonsToDisable:
			buttonToDisable.setCursor(QtGui.QCursor(QtCore.Qt.ForbiddenCursor))
			buttonToDisable.setStyleSheet('background-color: red;')
		wave = sa.WaveObject.from_wave_file(self.audioFile)
		play = wave.play()
		play.wait_done()
		if self.restore:
			ongoingSpeech = False


# class CaptureImage(QtCore.QThread, Helper):
# 	def __init__(self, label_userImage, label_captureStatus, values, buttonsToDisable=[]):
# 		QtCore.QThread.__init__(self)
# 		self.label_userImage = label_userImage
# 		self.label_captureStatus = label_captureStatus
# 		self.data = values
# 		self.buttonsToDisable = buttonsToDisable
#
# 	def run(self):
# 		camera_port = 0
# 		camera = cv2.VideoCapture(camera_port)
# 		time.sleep(1)  # the image will be dark if you don't wait
# 		_, capturedImage = camera.read()
#
# 		invertedImage = cv2.cvtColor(capturedImage, cv2.COLOR_BGR2RGB)
# 		image = Image.fromarray(invertedImage)
# 		image.save('data/object_detection/test_images/img.jpg')
# 		numImages = len(next(os.walk('data/user/images'))[2])
# 		if 'Session number' in self.data:
# 			image.save('data/user/images/S{}P{}.jpg'.format(self.data['Session number'], numImages + 1))
# 		del(camera)  # so that others can use the camera as soon as possible
#
# 		# update the capture status
# 		label = 'Your picture has been captured.'
# 		self.label_captureStatus.setText(label)
#
# 		# update the QtWidgets.QLabel to show the captured image
# 		pixmap_userImage = QtGui.QPixmap('data/object_detection/test_images/img.jpg')
# 		self.label_userImage.setPixmap(pixmap_userImage.scaledToWidth(self.WIDTH * 0.4, QtCore.Qt.SmoothTransformation))
#
# 		global ongoingSpeech
# 		ongoingSpeech = False
# 		return
#
#
# class HeadsetPlacementVerification(QtCore.QThread, Helper):
# 	def __init__(self, label_headsetPlacementResult, label_headsetPlacementStatus, buttonsToDisable=[]):
# 		QtCore.QThread.__init__(self)
# 		self.label_headsetPlacementStatus = label_headsetPlacementStatus
# 		self.label_headsetPlacementResult = label_headsetPlacementResult
# 		self.buttonsToDisable = buttonsToDisable
#
# 	def run(self):
# 		self.modelPreparation()
# 		self.loadFrozenTensorflowModel()
# 		self.loadLabelMap()
# 		self.verifyHeadsetPlacement()
# 		return
#
# 	def modelPreparation(self):
# 		# MODEL_NAME = 'faster_rcnn_inception_v2_coco_2018_05_26'
# 		MODEL_NAME = 'faster_rcnn_inception_v2_coco_2018_05_27'
#
# 		# path to frozen detection graph
# 		# this is the actual model that is used for the object detection
# 		self.PATH_TO_CKPT = 'data/object_detection/' + MODEL_NAME + '/frozen_inference_graph.pb'
#
# 		# list of the strings that is used to add correct label for each box.
# 		self.PATH_TO_LABELS = 'data/object_detection/data/tDCS_label_map.pbtxt'
#
# 		# self.NUM_CLASSES = 2
# 		self.NUM_CLASSES = 1
#
# 	def loadFrozenTensorflowModel(self):
# 		self.detection_graph = tf.Graph()
# 		with self.detection_graph.as_default():
# 			od_graph_def = tf.GraphDef()
# 			with tf.gfile.GFile(self.PATH_TO_CKPT, 'rb') as fid:
# 				serialized_graph = fid.read()
# 				od_graph_def.ParseFromString(serialized_graph)
# 				tf.import_graph_def(od_graph_def, name='')
#
# 	def loadLabelMap(self):
# 		label_map = label_map_util.load_labelmap(self.PATH_TO_LABELS)
# 		categories = label_map_util.convert_label_map_to_categories(label_map,
# 						max_num_classes=self.NUM_CLASSES, use_display_name=True)
# 		self.category_index = label_map_util.create_category_index(categories)
#
# 	def loadImageIntoNumpyArray(self, image):
# 		(im_width, im_height) = image.size
# 		return np.array(image.getdata()).reshape((im_height, im_width, 3)).astype(np.uint8)
#
# 	def runInferenceForSingleImage(self, image, graph):
# 		with graph.as_default():
# 			with tf.Session() as sess:
# 				# get handles to input and output tensors
# 				ops = tf.get_default_graph().get_operations()
# 				all_tensor_names = {output.name for op in ops for output in op.outputs}
# 				tensor_dict = {}
# 				for key in ['num_detections', 'detection_boxes', 'detection_scores',
# 					'detection_classes', 'detection_masks'
# 				]:
# 					tensor_name = key + ':0'
# 					if tensor_name in all_tensor_names:
# 						tensor_dict[key] = tf.get_default_graph().get_tensor_by_name(tensor_name)
# 				if 'detection_masks' in tensor_dict:
# 					# processing single image
# 					detection_boxes = tf.squeeze(tensor_dict['detection_boxes'], [0])
# 					detection_masks = tf.squeeze(tensor_dict['detection_masks'], [0])
# 					# reframe is required to translate mask from box coordinates to image
# 					# coordinates and fit the image size
# 					real_num_detection = tf.cast(tensor_dict['num_detections'][0], tf.int32)
# 					detection_boxes = tf.slice(detection_boxes, [0, 0], [real_num_detection, -1])
# 					detection_masks = tf.slice(detection_masks, [0, 0, 0], [real_num_detection, -1, -1])
# 					detection_masks_reframed = utils_ops.reframe_box_masks_to_image_masks(
# 						detection_masks, detection_boxes, image.shape[0], image.shape[1])
# 					detection_masks_reframed = tf.cast(
# 						tf.greater(detection_masks_reframed, 0.5), tf.uint8)
# 					# follow the convention by adding back the batch dimension
# 					tensor_dict['detection_masks'] = tf.expand_dims(
# 						detection_masks_reframed, 0)
# 				image_tensor = tf.get_default_graph().get_tensor_by_name('image_tensor:0')
#
# 				# run inference
# 				output_dict = sess.run(tensor_dict,
# 										feed_dict={image_tensor: np.expand_dims(image, 0)})
#
# 				# all outputs are float32 numpy arrays, so convert types as appropriate
# 				output_dict['num_detections'] = int(output_dict['num_detections'][0])
# 				output_dict['detection_classes'] = output_dict[
# 					'detection_classes'][0].astype(np.uint8)
# 				output_dict['detection_boxes'] = output_dict['detection_boxes'][0]
# 				output_dict['detection_scores'] = output_dict['detection_scores'][0]
# 				if 'detection_masks' in output_dict:
# 					output_dict['detection_masks'] = output_dict['detection_masks'][0]
#
# 		return output_dict
#
# 	def detectNose(self, image_np):
# 		# initialize dlib's face detector (HOG-based) and then create the facial landmark predictor
# 		detector = dlib.get_frontal_face_detector()
# 		predictor = dlib.shape_predictor('data/object_detection/shape_predictor_5_face_landmarks.dat')
# 		gray = cv2.cvtColor(image_np, cv2.COLOR_BGR2GRAY)
# 		# detect faces in the grayscale frame
# 		rects = detector(gray, 0)
# 		if len(rects) == 1:
# 			# determine the facial landmarks for the face region, then convert the facial landmark (x,y)-coordinates to a numpy array
# 			shape = predictor(gray, rects[0])
# 			shape = imutils.face_utils.shape_to_np(shape)
# 			nose = (shape[4][0], shape[4][1])
# 			return nose, len(rects)
# 		else:
# 			# no or more than 1 face found
# 			return None, len(rects)
#
# 	def validHeadsetPlacement(self, nasion, nose, x):
# 		start = nasion[0][1] * x
# 		end = nasion[0][3] * x
# 		# width = end - start
# 		# middle 50 percent width of detected nasion area
# 		# start += (0.25 * width)
# 		# end -= (0.25 * width)
# 		if start <= nose[0] <= end:
# 			return True
# 		else:
# 			return False
#
# 	def verifyHeadsetPlacement(self):
# 		image = Image.open('data/object_detection/test_images/img.jpg')
# 		# the array based representation of the image will be used later in order to prepare the
# 		# result image with boxes and labels on it
# 		image_np = self.loadImageIntoNumpyArray(image)
# 		y, x, d = image_np.shape
# 		# nose detection
# 		nose, num_faces = self.detectNose(image_np)
# 		# expand dimensions since the model expects images to have shape: [1, None, None, 3]
# 		# image_np_expanded = np.expand_dims(image_np, axis=0)
# 		# actual nasion detection
# 		output_dict = self.runInferenceForSingleImage(image_np, self.detection_graph)
# 		nasion = output_dict['detection_boxes']  # coordinates of the detected nasion
# 		# verifying nasion detection
# 		if len(nasion) != 1:
# 			self.label_headsetPlacementStatus.setText('tDCS headset is placed incorrectly.')
# 		# else:
# 			# calculate nasion center
# 			# p1 = (int(nasion[0][1] * x), int(nasion[0][0] * y))
# 			# p2 = (int(nasion[0][3] * x), int(nasion[0][2] * y))
# 			# visualization of the results of a nasion detection
# 			# cv2.rectangle(image_np, p1, p2, (0, 255, 0), 2)
# 		# verifying nose detection
# 		if nose is None:
# 			self.label_headsetPlacementStatus.setText('tDCS headset is placed incorrectly.')
# 		else:
# 			# visualization of the nose detection
# 			# cv2.circle(image_np, nose, 3, (0, 255, 0), -1)
# 			# validate the tDCS headset placement
# 			if self.validHeadsetPlacement(nasion, nose, x):
# 				self.label_headsetPlacementStatus.setText('tDCS headset is placed correctly.')
# 			else:
# 				self.label_headsetPlacementStatus.setText('tDCS headset is placed incorrectly.')
#
# 		# visualization of the results of a detection
# 		# vis_util.visualize_boxes_and_labels_on_image_array(
# 		# 	image_np,
# 		# 	output_dict['detection_boxes'],
# 		# 	output_dict['detection_classes'],
# 		# 	output_dict['detection_scores'],
# 		# 	self.category_index,
# 		# 	instance_masks=output_dict.get('detection_masks'),
# 		# 	use_normalized_coordinates=True,
# 		# 	line_thickness=8)
#
# 		max_index = np.argmax(output_dict['detection_scores'])
# 		# pred_class = output_dict['detection_classes'][max_index]
# 		print('Maximum Score:', output_dict['detection_scores'][max_index]*100)
#
# 		# save the verified image
# 		# image = Image.fromarray(image_np)
# 		# image.save('data/object_detection/test_images/img.jpg')
#
# 		# update the verified placement status
# 		# if pred_class == 1:
# 		# 	self.label_headsetPlacementStatus.setText('tDCS headset is placed correctly.')
# 		# else:
# 		# 	self.label_headsetPlacementStatus.setText('tDCS headset is placed incorrectly.')
#
# 		# update the QtWidgets.QLabel to show the verified image
# 		pixmap_headsetPlacementResult = QtGui.QPixmap('data/object_detection/test_images/img.jpg')
# 		self.label_headsetPlacementResult.setPixmap(pixmap_headsetPlacementResult.scaledToWidth(
# 			self.WIDTH * 0.4, QtCore.Qt.SmoothTransformation))
#
# 		global ongoingSpeech
# 		ongoingSpeech = False
# 		return


class CustomDialog(QtWidgets.QDialog, Helper):
	def __init__(self, parent=None, title='Intensity', labelText=''):
		super(CustomDialog, self).__init__(parent)

		# set the background color of the window
		palette = QtGui.QPalette()
		palette.setColor(QtGui.QPalette.Background, QtGui.QColor('#57068C'))
		self.setPalette(palette)

		# set window's icon and title
		self.setWindowIcon(QtGui.QIcon('data/images/logo.ico'))
		self.setWindowTitle(title)

		self.addWindowOnTopFlag()

		self.intensityLevel = 0

		label = labelText
		label_intensity = QtWidgets.QLabel(label)
		self.setFontStyle(label_intensity)

		# add numeric pain scale image to QtWidgets.QLabel
		visual_numeric_pain = QtWidgets.QLabel(self)
		pixmap_numeric_pain = QtGui.QPixmap('data/images/numeric_pain_scale.jpg')
		visual_numeric_pain.setPixmap(pixmap_numeric_pain.scaledToWidth(self.WIDTH * 0.4, QtCore.Qt.SmoothTransformation))

		self.radioButtonList_preSideEffectIntensity = []
		radioButton_layout = QtWidgets.QHBoxLayout()
		radioButton_group = QtWidgets.QButtonGroup(self)
		radioButton_group.setExclusive(True)
		for i in range(11):
			radioButton = QtWidgets.QRadioButton(str(i))
			self.setRadioButtonStyle(radioButton)
			radioButton_group.addButton(radioButton, i)
			self.radioButtonList_preSideEffectIntensity.append(radioButton)
			radioButton_layout.addWidget(radioButton)
			radioButton.toggled.connect(lambda:self.recordRadioButtonSelectionCustomDialog(
				self.radioButtonList_preSideEffectIntensity))
		self.setRadioButtonLayoutStyle(radioButton_layout)

		sideEffectIntensity_layout = QtWidgets.QVBoxLayout()
		sideEffectIntensity_layout.addWidget(label_intensity)
		sideEffectIntensity_layout.addWidget(visual_numeric_pain, QtCore.Qt.AlignCenter, QtCore.Qt.AlignCenter)
		sideEffectIntensity_layout.addLayout(radioButton_layout)
		self.setVisualAnalogScaleSpacing(sideEffectIntensity_layout)

		sideEffectIntensity_layout.setContentsMargins(self.WIDTH * 0, self.HEIGHT * 0.02, self.WIDTH * 0, self.HEIGHT * 0.04)

		button_ok = QtWidgets.QPushButton('OK')
		button_cancel = QtWidgets.QPushButton('Cancel')

		buttons = [button_ok, button_cancel]
		button_layout = QtWidgets.QHBoxLayout()  # create a horizontal layout to hold buttons

		for button in buttons:
			self.setButtonStyle(button)
			button_layout.addWidget(button)

		# create a vertical layout to hold widgets
		layout = QtWidgets.QVBoxLayout()
		layout.addWidget(label_intensity)
		layout.addLayout(sideEffectIntensity_layout)
		layout.addLayout(button_layout)

		# set dialog layout
		self.setLayout(layout)

		# button click connections
		button_ok.clicked.connect(self.ok)
		button_cancel.clicked.connect(self.cancel)

	def recordRadioButtonSelectionCustomDialog(self, radioButtonList):
		for radioButton in radioButtonList:
			if radioButton.isChecked():
				self.intensityLevel = int(radioButton.text())
				radioButton.setStyleSheet('color: red;')
			else:
				radioButton.setStyleSheet('color: white;')

	def ok(self):
		selected = False
		for radioButton in self.radioButtonList_preSideEffectIntensity:
			if radioButton.isChecked():
				selected = True
				break
		if not selected:
			QtWidgets.QMessageBox.critical(self, 'Intensity',
				'Please enter the intensity before continuing further.', QtWidgets.QMessageBox.Ok)
		else:
			self.accept()

	def cancel(self):
		self.intensityLevel = 0
		self.reject()

	def getIntensityLevel(self):
		return self.intensityLevel


class MainWindow(QtWidgets.QMainWindow, Helper):
	def __init__(self, parent=None):
		super(MainWindow, self).__init__(parent)  # call the super class constructor

		QtWidgets.QApplication.setStyle(QtWidgets.QStyleFactory.create('fusion'))
		self.setWindowTitle('tDCS')
		self.setFixedSize(self.WIDTH * 0.42, self.HEIGHT * 0.80)

		self.addWindowOnTopFlag()

		# set the background color of the window
		palette = QtGui.QPalette()
		palette.setColor(QtGui.QPalette.Background, QtGui.QColor('#57068C'))
		self.setPalette(palette)

		# set window's icon
		self.setWindowIcon(QtGui.QIcon('data/images/logo.ico'))

		# add a toolbar
		self.addActionToolBar()

		self.allowExit = True
		self.minBatteryRequired = 20

		# audio configurations
		global ongoingSpeech
		ongoingSpeech = False
		self.audioPath = 'data/sound/voice1/'
		self.isMute = False
		self.button_replay = QtWidgets.QPushButton('Replay')
		self.button_replay.clicked.connect(self.replayAudio)

		self.studyID = None
		self.dataSaved = False
		self.dataSent = False
		self.PORTAL_PASSWORD = 'krupp123'

		self.welcomeLayout()
		self.stacked_layout.addWidget(self.welcome_widget)

		# set the central widget to display the layout
		central_widget = QtWidgets.QWidget()
		central_widget.setLayout(self.stacked_layout)
		self.setCentralWidget(central_widget)

	def welcomeLayout(self):
		# welcome layout of the window
		label1 = 'Welcome to your tDCS Session!'
		label2 = 'Are you ready to begin?'
		label_welcome = QtWidgets.QLabel(label1)
		self.setFontStyle(label_welcome)
		label_ready = QtWidgets.QLabel(label2)
		self.setFontStyle(label_ready)

		label_studyID = QtWidgets.QLabel('Enter your study ID: \t')
		self.setFontStyle(label_studyID)
		self.lineEdit_studyID = QtWidgets.QLineEdit()
		self.setLineEditStyle(self.lineEdit_studyID, widthFactor=0.18)
		if not self.FIRST_SESSION:
			self.lineEdit_studyID.setText(str(self.user_data['Study ID'].iloc[-1]))

		studyID_layout = QtWidgets.QHBoxLayout()
		studyID_layout.addWidget(label_studyID)
		studyID_layout.addWidget(self.lineEdit_studyID)
		studyID_layout.setContentsMargins(self.WIDTH * 0.015, self.HEIGHT * 0.01, self.WIDTH * 0.015, self.HEIGHT * 0.01)

		label_nameTechnician = QtWidgets.QLabel('Enter name of the study technician:')
		self.setFontStyle(label_nameTechnician)
		self.lineEdit_nameTechnician = QtWidgets.QLineEdit()
		self.setLineEditStyle(self.lineEdit_nameTechnician, widthFactor=0.18)
		nameTechnician_layout = QtWidgets.QHBoxLayout()
		nameTechnician_layout.addWidget(label_nameTechnician)
		nameTechnician_layout.addWidget(self.lineEdit_nameTechnician)
		nameTechnician_layout.setContentsMargins(self.WIDTH * 0.015, self.HEIGHT * 0.01, self.WIDTH * 0.015, self.HEIGHT * 0.01)

		label_emailTechnician = QtWidgets.QLabel('Enter email of the study technician:')
		self.setFontStyle(label_emailTechnician)

		with open('data/email/technicians.txt', 'r') as file: file_contents = file.read()
		technicianEmails = file_contents.split('\n')

		self.dropDown_technicianEmail = QtWidgets.QComboBox()
		self.setComboBoxStyle(self.dropDown_technicianEmail, widthFactor=0.18)
		for technicianEmail in technicianEmails:
			self.dropDown_technicianEmail.addItem(technicianEmail)
		self.dropDown_technicianEmail.currentIndexChanged.connect(self.selectedTechnicianEmail)
		self.studyTechnicianEmail = ''

		emailTechnician_layout = QtWidgets.QHBoxLayout()
		emailTechnician_layout.addWidget(label_emailTechnician)
		emailTechnician_layout.addWidget(self.dropDown_technicianEmail)
		emailTechnician_layout.setContentsMargins(self.WIDTH * 0.015, self.HEIGHT * 0.01, self.WIDTH * 0.015, self.HEIGHT * 0.25)

		button_portal = QtWidgets.QPushButton('Portal')
		button_next = QtWidgets.QPushButton('Next')

		buttons = [button_portal, self.button_replay, button_next]
		button_layout = QtWidgets.QHBoxLayout()  # create a horizontal layout to hold buttons

		for button in buttons:
			self.setButtonStyle(button)
			button_layout.addWidget(button)

		# create a vertical layout to hold widgets
		welcome_layout = QtWidgets.QVBoxLayout()
		welcome_layout.addWidget(label_welcome)
		welcome_layout.addWidget(label_ready)
		welcome_layout.addLayout(studyID_layout)
		welcome_layout.addLayout(nameTechnician_layout)
		welcome_layout.addLayout(emailTechnician_layout)
		welcome_layout.addLayout(button_layout)

		# create a widget to display the layout
		self.welcome_widget = QtWidgets.QWidget()
		self.welcome_widget.setLayout(welcome_layout)

		# start the audio
		self.audioFile = self.audioPath + 'welcome.wav'
		self.buttonsToDisable = buttons
		if not self.isMute: self.playAudio()

		# button click connections
		button_portal.clicked.connect(self.startPortalLayout)
		button_next.clicked.connect(self.startHeadsetLayout)

	def startPortalLayout(self):
		global ongoingSpeech
		if not ongoingSpeech:
			self.removeWindowOnTopFlag()
			inputDialog, ok = self.createTextDialog(title='Login', echoMode=QtWidgets.QLineEdit.Password,
				label='Please enter password to access the portal: \t\t')
			password = inputDialog.textValue()
			if ok:
				if password == self.PORTAL_PASSWORD:
					self.portalLayout()  # create the portal layout
					self.stacked_layout.addWidget(self.portal_widget)  # add this to the stacked layout
					self.stacked_layout.setCurrentIndex(self.index)  # change the visible layout in the stack
					self.index += 1
				else:
					choice = QtWidgets.QMessageBox.critical(self, 'Incorrect Password',
						'The password you have entered is incorrect. Please try again.', QtWidgets.QMessageBox.Retry | QtWidgets.QMessageBox.Cancel)
					if choice == QtWidgets.QMessageBox.Retry:
						self.startPortalLayout()
			self.addWindowOnTopFlag()

	def portalLayout(self):
		label_subjectID = QtWidgets.QLabel('Please enter the subject\'s master ID:')
		label_subjectStudy = QtWidgets.QLabel('Please enter the study the subject is in:')
		label_subjectSession = QtWidgets.QLabel('Please enter the subject\'s session number:')
		label_subjectDose = QtWidgets.QLabel('Please enter the subject\'s allocated tDCS dose (i.e., 1.5 mA):')
		label_subjectDuration = QtWidgets.QLabel('Please enter the subject\'s allocated tDCS dose duration (i.e., 20 minutes):')
		label_subjectRegimen = QtWidgets.QLabel('Please enter the subject\'s training regimen (i.e., Motor, BrainHQ):')
		label_subjectBaseline = QtWidgets.QLabel('When was the subject\'s baseline examination:')

		self.lineEdit_subjectID = QtWidgets.QLineEdit()
		self.lineEdit_subjectStudy = QtWidgets.QLineEdit()
		self.lineEdit_subjectSession = QtWidgets.QLineEdit()
		self.lineEdit_subjectDose = QtWidgets.QLineEdit()
		self.lineEdit_subjectDuration = QtWidgets.QLineEdit()
		self.lineEdit_subjectRegimen = QtWidgets.QLineEdit()
		self.lineEdit_subjectBaseline = QtWidgets.QLineEdit()

		# create a vertical layout to hold widgets
		portal_layout = QtWidgets.QVBoxLayout()

		labels = [label_subjectID, label_subjectStudy, label_subjectSession, label_subjectDose,
				  label_subjectDuration, label_subjectRegimen, label_subjectBaseline]
		lineEdits = [self.lineEdit_subjectID, self.lineEdit_subjectStudy, self.lineEdit_subjectSession, self.lineEdit_subjectDose,
					 self.lineEdit_subjectDuration, self.lineEdit_subjectRegimen, self.lineEdit_subjectBaseline]

		for label, lineEdit in zip(labels, lineEdits):
			self.setFontStyle(label, size=15)
			self.setLineEditStyle(lineEdit)
			layout = QtWidgets.QHBoxLayout()
			layout.addWidget(label)
			layout.addWidget(lineEdit)
			portal_layout.addLayout(layout)

		if self.FIRST_SESSION and self.lineEdit_subjectDuration.text().strip() == '':
			self.lineEdit_subjectDuration.setText('20')

		if 'Master ID' in self.values:
			self.lineEdit_subjectID.setText(str(self.values['Master ID']))
			self.lineEdit_subjectStudy.setText(str(self.values['Subject study']))
			self.lineEdit_subjectSession.setText(str(self.values['Session number']))
			self.lineEdit_subjectDose.setText(str(self.values['Subject tDCS dose']))
			self.lineEdit_subjectDuration.setText(str(self.values['Subject tDCS dose duration']))
			self.lineEdit_subjectRegimen.setText(str(self.values['Subject training regimen']))
			self.lineEdit_subjectBaseline.setText(str(self.values['Subject baseline examination']))
		elif not self.FIRST_SESSION:
			self.lineEdit_subjectID.setText(str(self.user_data['Master ID'].iloc[-1]))
			self.lineEdit_subjectStudy.setText(str(self.user_data['Subject study'].iloc[-1]))
			self.lineEdit_subjectSession.setText(str(int(self.user_data['Session number'].iloc[-1] + 1)))
			self.lineEdit_subjectDose.setText(str(self.user_data['Subject tDCS dose'].iloc[-1]))
			self.lineEdit_subjectDuration.setText(str(self.user_data['Subject tDCS dose duration'].iloc[-1]))
			self.lineEdit_subjectRegimen.setText(str(self.user_data['Subject training regimen'].iloc[-1]))
			self.lineEdit_subjectBaseline.setText(str(self.user_data['Subject baseline examination'].iloc[-1]))

		button_done = QtWidgets.QPushButton('Done')

		buttons = [button_done]
		button_layout = QtWidgets.QHBoxLayout()  # create a horizontal layout to hold buttons

		for button in buttons:
			self.setButtonStyle(button)
			button_layout.addWidget(button)

		portal_layout.addLayout(button_layout)

		# create a widget to display the layout
		self.portal_widget = QtWidgets.QWidget()
		self.portal_widget.setLayout(portal_layout)

		# start the audio
		self.buttonsToDisable = buttons

		# button click connections
		button_done.clicked.connect(self.restartWelcomeLayout)

	def restartWelcomeLayout(self):
		global ongoingSpeech
		if not ongoingSpeech:
			self.values['Master ID'] = self.lineEdit_subjectID.text().strip()
			self.values['Subject study'] = self.lineEdit_subjectStudy.text().strip()
			try:
				self.values['Session number'] = int(self.lineEdit_subjectSession.text().strip())
			except ValueError:
				QtWidgets.QMessageBox.critical(self, 'Session number',
					'The session number entered is invalid. Please correct it before continuing further.', QtWidgets.QMessageBox.Ok)
				return
			self.values['Subject tDCS dose'] = self.lineEdit_subjectDose.text().strip()
			try:
				self.values['Subject tDCS dose duration'] = float(self.lineEdit_subjectDuration.text().strip())
			except ValueError:
				QtWidgets.QMessageBox.critical(self, 'Dose duration',
					'The dose duration entered is invalid. Please correct it before continuing further.', QtWidgets.QMessageBox.Ok)
				return
			self.values['Subject training regimen'] = self.lineEdit_subjectRegimen.text().strip()
			self.values['Subject baseline examination'] = self.lineEdit_subjectBaseline.text().strip()
			self.stacked_layout.removeWidget(self.stacked_layout.currentWidget())  # remove this from the stacked layout
			self.index = 0
			self.stacked_layout.setCurrentIndex(self.index)  # change the visible layout in the stack
			self.index += 1

	def startHeadsetLayout(self):
		global ongoingSpeech
		if not ongoingSpeech:
			battery_sufficient, plugged = self.checkBattery()
			self.studyID = self.lineEdit_studyID.text().strip().replace(' ','')
			self.studyTechnicianName = self.lineEdit_nameTechnician.text().strip()
			# self.studyTechnicianEmail = self.lineEdit_emailTechnician.text().strip()

			EMAIL_REGEX = re.compile(r'[^@]+@[^@]+\.[^@]+')

			if not battery_sufficient and not plugged:
				choice = QtWidgets.QMessageBox.critical(self, 'Low battery',
					'Please charge the device to at least {}% to continue'.format(self.minBatteryRequired),
					QtWidgets.QMessageBox.Retry | QtWidgets.QMessageBox.Cancel | QtWidgets.QMessageBox.Abort | QtWidgets.QMessageBox.Help, QtWidgets.QMessageBox.Retry)
				if choice == QtWidgets.QMessageBox.Retry:
					self.startHeadsetLayout()
				elif choice == QtWidgets.QMessageBox.Abort:
					self.exitApplication(self.studyID)
				elif choice == QtWidgets.QMessageBox.Help:
					self.help(self.studyID)
			elif self.studyID == '':
				QtWidgets.QMessageBox.critical(self, 'Study ID',
					'Please enter your study ID before continuing further.', QtWidgets.QMessageBox.Ok)
			elif self.studyTechnicianName == '':
				QtWidgets.QMessageBox.critical(self, 'Technician Name',
					'Please enter name of the technician before continuing further.', QtWidgets.QMessageBox.Ok)
			elif self.studyTechnicianEmail != '' and not EMAIL_REGEX.fullmatch(self.studyTechnicianEmail):
				QtWidgets.QMessageBox.critical(self, 'Technician Email',
					'The study technician\'s email is invalid. Please correct it before continuing further.', QtWidgets.QMessageBox.Ok)
			elif self.FIRST_SESSION and not self.isValidPortalInfo():
				QtWidgets.QMessageBox.critical(self, 'Subject Information',
					'Please go to the portal and enter all subject information before continuing further.', QtWidgets.QMessageBox.Ok)
			else:
				self.values['Study ID'] = self.studyID
				self.values['Study technician'] = self.studyTechnicianName
				if 'Master ID' not in self.values:
					self.values['Master ID'] = self.user_data['Master ID'].iloc[-1]
					self.values['Subject study'] = self.user_data['Subject study'].iloc[-1]
					self.values['Session number'] = int(self.user_data['Session number'].iloc[-1]) + 1
					self.values['Subject tDCS dose'] = self.user_data['Subject tDCS dose'].iloc[-1]
					self.values['Subject tDCS dose duration'] = str(self.user_data['Subject tDCS dose duration'].iloc[-1])
					self.values['Subject training regimen'] = self.user_data['Subject training regimen'].iloc[-1]
					self.values['Subject baseline examination'] = self.user_data['Subject baseline examination'].iloc[-1]

				# self.headsetLayout()  # create the headset layout
				# self.stacked_layout.addWidget(self.headset_widget)  # add this to the stacked layout
				self.preSessionHeadsetPainLayout()  # create the pre-session headset pain layout
				self.stacked_layout.addWidget(self.preSessionHeadsetPain_widget)  # add this to the stacked layout
				self.stacked_layout.setCurrentIndex(self.index)  # change the visible layout in the stack
				self.index += 1

	# def headsetLayout(self):
	# 	label1 = 'Are your headset and device prepared?'
	# 	label_headset = QtWidgets.QLabel(label1)
	# 	self.setFontStyle(label_headset)
	#
	# 	# add the reference image to QtWidgets.QLabel
	# 	reference_image = QtWidgets.QLabel(self)
	# 	pixmap_headset = QtGui.QPixmap('data/images/headset_placement.png')
	# 	reference_image.setPixmap(pixmap_headset.scaledToWidth(self.WIDTH * 0.25, QtCore.Qt.SmoothTransformation))
	#
	# 	label2 = 'Click "Yes" to take photo'
	# 	label_warning = QtWidgets.QLabel(label2)
	# 	self.setFontStyle(label_warning)
	#
	# 	button_back = QtWidgets.QPushButton('Back')
	# 	button_no = QtWidgets.QPushButton('No')
	# 	button_yes = QtWidgets.QPushButton('Yes')
	#
	# 	buttons = [button_back, self.button_replay, button_no, button_yes]
	# 	button_layout = QtWidgets.QHBoxLayout()  # create a horizontal layout to hold buttons
	#
	# 	for button in buttons:
	# 		self.setButtonStyle(button)
	# 		button_layout.addWidget(button)
	#
	# 	# create a vertical layout to hold widgets
	# 	headset_layout = QtWidgets.QVBoxLayout()
	# 	headset_layout.addWidget(label_headset)
	# 	headset_layout.addWidget(reference_image, QtCore.Qt.AlignCenter, QtCore.Qt.AlignCenter)
	# 	headset_layout.addWidget(label_warning, QtCore.Qt.AlignCenter, QtCore.Qt.AlignCenter)
	# 	headset_layout.addLayout(button_layout)
	#
	# 	# create a widget to display the layout
	# 	self.headset_widget = QtWidgets.QWidget()
	# 	self.headset_widget.setLayout(headset_layout)
	#
	# 	# start the audio
	# 	self.audioFile = self.audioPath + 'headset_prepared.wav'
	# 	self.buttonsToDisable = buttons
	# 	if not self.isMute: self.playAudio()
	#
	# 	# button click connections
	# 	button_back.clicked.connect(self.gotoPreviousWidget)
	# 	button_no.clicked.connect(self.headsetPlacementIssue)
	# 	button_yes.clicked.connect(self.startWebcamStreamingLayout)
	#
	# def startWebcamStreamingLayout(self):
	# 	global ongoingSpeech
	# 	if not ongoingSpeech:
	# 		self.webcamStreamingLayout()  # create the webstream layout
	# 		self.stacked_layout.addWidget(self.captureImage_widget)  # add this to the stacked layout
	# 		self.stacked_layout.setCurrentIndex(self.index)  # change the visible layout in the stack
	# 		self.index += 1
	#
	# def webcamStreamingLayout(self):
	# 	label = 'Capturing your picture...'
	# 	label_captureStatus = QtWidgets.QLabel(label)
	# 	self.setFontStyle(label_captureStatus)
	#
	# 	# create a QtWidgets.QLabel for user's captured image
	# 	label_userImage = QtWidgets.QLabel(self)
	#
	# 	button_back = QtWidgets.QPushButton('Back')
	# 	button_retry = QtWidgets.QPushButton('Retry')
	# 	button_next = QtWidgets.QPushButton('Verify')
	#
	# 	buttons = [button_back, button_retry, button_next]
	# 	button_layout = QtWidgets.QHBoxLayout()  # create a horizontal layout to hold buttons
	#
	# 	for button in buttons:
	# 		self.setButtonStyle(button)
	# 		button_layout.addWidget(button)
	# 		button.setCursor(QtGui.QCursor(QtCore.Qt.ForbiddenCursor))
	# 		button.setStyleSheet('background-color: red;')
	#
	# 	global ongoingSpeech
	# 	ongoingSpeech = True
	#
	# 	# capture the user's facial image
	# 	self.captureImage = CaptureImage(label_userImage, label_captureStatus, self.values, buttons)
	# 	self.captureImage.finished.connect(self.restoreButtons)
	# 	self.captureImage.start()
	#
	# 	# create a vertical layout to hold widgets
	# 	captureImage_layout = QtWidgets.QVBoxLayout()
	# 	captureImage_layout.addWidget(label_captureStatus)
	# 	captureImage_layout.addWidget(label_userImage, QtCore.Qt.AlignCenter, QtCore.Qt.AlignCenter)
	# 	captureImage_layout.addLayout(button_layout)
	#
	# 	# create a widget to display the layout
	# 	self.captureImage_widget = QtWidgets.QWidget()
	# 	self.captureImage_widget.setLayout(captureImage_layout)
	#
	# 	self.buttonsToDisable = buttons
	#
	# 	# button click connections
	# 	button_back.clicked.connect(self.gotoPreviousWidget)
	# 	button_retry.clicked.connect(self.captureImageAgain)
	# 	button_next.clicked.connect(self.startHeadsetPlacementVerificationLayout)
	#
	# def captureImageAgain(self):
	# 	global ongoingSpeech
	# 	if not ongoingSpeech:
	# 		self.index -= 1
	# 		self.stacked_layout.removeWidget(self.captureImage_widget)  # remove this from the stacked layout
	# 		self.startWebcamStreamingLayout()
	#
	# def startHeadsetPlacementVerificationLayout(self):
	# 	global ongoingSpeech
	# 	if not ongoingSpeech:
	# 		self.headsetPlacementVerificationLayout()  # create the headset placement verification layout
	# 		self.stacked_layout.addWidget(self.headsetPlacementVerification_widget)  # add this to the stacked layout
	# 		self.stacked_layout.setCurrentIndex(self.index)  # change the visible layout in the stack
	# 		self.index += 1
	#
	# def headsetPlacementVerificationLayout(self):
	# 	label = 'Verifying your tDCS headset placement...'
	# 	label_headsetPlacementStatus = QtWidgets.QLabel(label)
	# 	self.setFontStyle(label_headsetPlacementStatus)
	#
	# 	# create a QtWidgets.QLabel for headset placement result image
	# 	label_headsetPlacementResult = QtWidgets.QLabel(self)
	#
	# 	button_retry = QtWidgets.QPushButton('Retry')
	# 	button_next = QtWidgets.QPushButton('Next')
	#
	# 	buttons = [self.button_replay, button_retry, button_next]
	# 	button_layout = QtWidgets.QHBoxLayout()  # create a horizontal layout to hold buttons
	#
	# 	for button in buttons:
	# 		self.setButtonStyle(button)
	# 		button_layout.addWidget(button)
	# 		button.setCursor(QtGui.QCursor(QtCore.Qt.ForbiddenCursor))
	# 		button.setStyleSheet('background-color: red;')
	#
	# 	global ongoingSpeech
	# 	ongoingSpeech = True
	#
	# 	# verify the tDCS headset placement
	# 	self.headsetPlacementVerification = HeadsetPlacementVerification(label_headsetPlacementResult, label_headsetPlacementStatus, buttons)
	# 	self.headsetPlacementVerification.finished.connect(self.restoreButtons)
	# 	self.headsetPlacementVerification.start()
	#
	# 	# create a vertical layout to hold widgets
	# 	headsetPlacementVerification_layout = QtWidgets.QVBoxLayout()
	# 	headsetPlacementVerification_layout.addWidget(label_headsetPlacementStatus)
	# 	headsetPlacementVerification_layout.addWidget(label_headsetPlacementResult, QtCore.Qt.AlignCenter, QtCore.Qt.AlignCenter)
	# 	headsetPlacementVerification_layout.addLayout(button_layout)
	#
	# 	# create a widget to display the layout
	# 	self.headsetPlacementVerification_widget = QtWidgets.QWidget()
	# 	self.headsetPlacementVerification_widget.setLayout(headsetPlacementVerification_layout)
	#
	# 	self.buttonsToDisable = buttons
	#
	# 	# button click connections
	# 	button_retry.clicked.connect(self.captureImageAgainAfterVerification)
	# 	button_next.clicked.connect(self.startPreSessionHeadsetPainLayout)
	#
	# def captureImageAgainAfterVerification(self):
	# 	global ongoingSpeech
	# 	if not ongoingSpeech:
	# 		self.index -= 2
	# 		self.stacked_layout.removeWidget(self.headsetPlacementVerification_widget)  # remove this from the stacked layout
	# 		self.stacked_layout.removeWidget(self.captureImage_widget)  # remove this from the stacked layout
	# 		self.startWebcamStreamingLayout()

	def startPreSessionHeadsetPainLayout(self):
		global ongoingSpeech
		if not ongoingSpeech:
			self.preSessionHeadsetPainLayout()  # create the pre-session headset pain layout
			self.stacked_layout.addWidget(self.preSessionHeadsetPain_widget)  # add this to the stacked layout
			self.stacked_layout.setCurrentIndex(self.index)  # change the visible layout in the stack
			self.index += 1

	def preSessionHeadsetPainLayout(self):
		label = 'Do you feel pain from the headset? Please enter the intensity of your pain.'
		label_headset_pain = QtWidgets.QLabel(label)
		self.setFontStyle(label_headset_pain)

		# add headset pain visual analogue scale image to QtWidgets.QLabel
		visual_headset_pain = QtWidgets.QLabel(self)
		pixmap_headset_pain = QtGui.QPixmap('data/images/visual_MS_pain.jpg')
		visual_headset_pain.setPixmap(pixmap_headset_pain.scaledToWidth(self.WIDTH * 0.4, QtCore.Qt.SmoothTransformation))

		self.radioButtonList_preHeadsetPain = []
		radioButton_layout = QtWidgets.QHBoxLayout()
		radioButton_group = QtWidgets.QButtonGroup(self)
		radioButton_group.setExclusive(True)
		for i in range(11):
			radioButton = QtWidgets.QRadioButton(str(i))
			self.setRadioButtonStyle(radioButton)
			radioButton_group.addButton(radioButton, i)
			self.radioButtonList_preHeadsetPain.append(radioButton)
			radioButton_layout.addWidget(radioButton)
			radioButton.toggled.connect(lambda:self.recordRadioButtonSelection(self.radioButtonList_preHeadsetPain, 'Pre-Session Headset Device Pain'))
		self.setRadioButtonLayoutStyle(radioButton_layout)

		headsetPainScale_layout = QtWidgets.QVBoxLayout()
		headsetPainScale_layout.addWidget(visual_headset_pain, QtCore.Qt.AlignCenter, QtCore.Qt.AlignCenter)
		headsetPainScale_layout.addLayout(radioButton_layout)
		self.setVisualAnalogScaleSpacing(headsetPainScale_layout)

		self.values['Pre-Session Headset Device Pain'] = 0

		button_back = QtWidgets.QPushButton('Back')
		button_next = QtWidgets.QPushButton('Next')

		buttons = [button_back, self.button_replay, button_next]
		button_layout = QtWidgets.QHBoxLayout()  # create a horizontal layout to hold buttons

		for button in buttons:
			self.setButtonStyle(button)
			button_layout.addWidget(button)

		# create a vertical layout to hold widgets
		preSessionHeadsetPain_layout = QtWidgets.QVBoxLayout()
		preSessionHeadsetPain_layout.addWidget(label_headset_pain)
		preSessionHeadsetPain_layout.addLayout(headsetPainScale_layout)
		preSessionHeadsetPain_layout.addLayout(button_layout)

		# create a widget to display the layout
		self.preSessionHeadsetPain_widget = QtWidgets.QWidget()
		self.preSessionHeadsetPain_widget.setLayout(preSessionHeadsetPain_layout)

		# start the audio
		self.audioFile = self.audioPath + 'headset_pain.wav'
		self.buttonsToDisable = buttons
		if not self.isMute: self.playAudio()

		# button click connections
		button_back.clicked.connect(self.gotoPreviousWidget)
		button_next.clicked.connect(self.startPreSessionSideEffectsExperiencedLayout)

	def startPreSessionSideEffectsExperiencedLayout(self):
		global ongoingSpeech
		if not ongoingSpeech:
			selected = False
			for radioButton in self.radioButtonList_preHeadsetPain:
				if radioButton.isChecked():
					selected = True
					break
			if not selected:
				QtWidgets.QMessageBox.critical(self, 'Pain from headset',
					'Please enter the intensity of your pain from the headset before continuing further.', QtWidgets.QMessageBox.Ok)
			else:
				if 'Pre-Session Headset Device Pain' not in self.values:
					self.values['Pre-Session Headset Device Pain'] = 0
				if int(self.values['Pre-Session Headset Device Pain']) >= self.PAIN_THRESHOLD:
					self.highPain(self.studyID)
				self.preSessionSideEffectsExperiencedLayout()  # create the pre-session side-effects experienced layout
				self.stacked_layout.addWidget(self.preSessionSideEffectsExperienced_widget)  # add this to the stacked layout
				self.stacked_layout.setCurrentIndex(self.index)  # change the visible layout in the stack
				self.index += 1

	def preSessionSideEffectsExperiencedLayout(self):
		self.preSessionSideEffects = True
		label = 'Did you experience any side effect(s) of the tDCS after your last treatment session ended?'
		label_pre_session_side_effects_experienced = QtWidgets.QLabel(label)
		self.setFontStyle(label_pre_session_side_effects_experienced)

		button_back = QtWidgets.QPushButton('Back')
		button_no = QtWidgets.QPushButton('No')
		button_yes = QtWidgets.QPushButton('Yes')

		buttons = [button_back, self.button_replay, button_no, button_yes]
		button_layout = QtWidgets.QHBoxLayout()  # create a horizontal layout to hold buttons

		for button in buttons:
			self.setButtonStyle(button)
			button_layout.addWidget(button)

		# create a vertical layout to hold widgets
		preSessionSideEffectsExperienced_layout = QtWidgets.QVBoxLayout()
		preSessionSideEffectsExperienced_layout.addWidget(label_pre_session_side_effects_experienced)
		preSessionSideEffectsExperienced_layout.addLayout(button_layout)

		# create a widget to display the layout
		self.preSessionSideEffectsExperienced_widget = QtWidgets.QWidget()
		self.preSessionSideEffectsExperienced_widget.setLayout(preSessionSideEffectsExperienced_layout)

		# start the audio
		self.audioFile = self.audioPath + 'sideEffects_lastSession.wav'
		self.buttonsToDisable = buttons
		if not self.isMute: self.playAudio()

		# button click connections
		button_back.clicked.connect(self.gotoPreviousWidget)
		button_no.clicked.connect(self.preSessionNoSideEffects)
		button_yes.clicked.connect(self.startPreSessionSideEffectsHeadsetRelatedLayout)

	def preSessionNoSideEffects(self):
		global ongoingSpeech
		if not ongoingSpeech:
			self.preSessionSideEffects = False
			sideEffects = ['Skin tingling', 'Skin itching', 'Sensations of warmth']
			for sideEffect in sideEffects:
				self.values['Intensity: Pre-Session ' + sideEffect] = 0
				self.values['Duration: Pre-Session ' + sideEffect] = 0
			self.values['Intensity: Pre-Session Other'] = []
			self.values['Duration: Pre-Session Other'] = []
			self.startPreSessionDiseasePainLayout()

	def startPreSessionSideEffectsHeadsetRelatedLayout(self):
		global ongoingSpeech
		if not ongoingSpeech:
			self.preSessionSideEffectsHeadsetRelatedLayout()  # create the pre-session headset related side-effects layout
			self.stacked_layout.addWidget(self.preSessionSideEffectsHeadset_widget)  # add this to the stacked layout
			self.stacked_layout.setCurrentIndex(self.index)  # change the visible layout in the stack
			self.index += 1

	def preSessionSideEffectsHeadsetRelatedLayout(self):
		# these values will be changed if they click 'No'
		self.headsetRelatedSideEffects = True
		self.values['Pre-Session Headset-Related Side Effects'] = 'Yes'

		label = 'Were any of the side effects related to the headset?'
		label_pre_session_side_effects_headset = QtWidgets.QLabel(label)
		self.setFontStyle(label_pre_session_side_effects_headset)

		button_back = QtWidgets.QPushButton('Back')
		button_no = QtWidgets.QPushButton('No')
		button_yes = QtWidgets.QPushButton('Yes')

		buttons = [button_back, self.button_replay, button_no, button_yes]
		button_layout = QtWidgets.QHBoxLayout()  # create a horizontal layout to hold buttons

		for button in buttons:
			self.setButtonStyle(button)
			button_layout.addWidget(button)

		# create a vertical layout to hold widgets
		preSessionSideEffectsHeadset_layout = QtWidgets.QVBoxLayout()
		preSessionSideEffectsHeadset_layout.addWidget(label_pre_session_side_effects_headset)
		preSessionSideEffectsHeadset_layout.addLayout(button_layout)

		# create a widget to display the layout
		self.preSessionSideEffectsHeadset_widget = QtWidgets.QWidget()
		self.preSessionSideEffectsHeadset_widget.setLayout(preSessionSideEffectsHeadset_layout)

		# start the audio
		# self.audioFile = self.audioPath + '.wav'
		# self.buttonsToDisable = buttons
		# if not self.isMute: self.playAudio()

		# button click connections
		button_back.clicked.connect(self.gotoPreviousWidget)
		button_no.clicked.connect(self.preSessionNoHeadsetRelatedSideEffects)
		button_yes.clicked.connect(self.startPreSessionSideEffectsLayout)

	def preSessionNoHeadsetRelatedSideEffects(self):
		global ongoingSpeech
		if not ongoingSpeech:
			self.headsetRelatedSideEffects = False
			self.values['Pre-Session Headset-Related Side Effects'] = 'No'
			sideEffects = ['Skin tingling', 'Skin itching', 'Sensations of warmth']
			for sideEffect in sideEffects:
				self.values['Intensity: Pre-Session ' + sideEffect] = 0
				self.values['Duration: Pre-Session ' + sideEffect] = 0
			self.preSessionSideEffectsLayout()  # create the pre-session side-effects layout
			self.stacked_layout.addWidget(self.preSessionSideEffects_widget)  # add this to the stacked layout
			self.stacked_layout.setCurrentIndex(self.index)  # change the visible layout in the stack
			self.index += 1

	def startPreSessionSideEffectsLayout(self):
		global ongoingSpeech
		if not ongoingSpeech:
			self.headsetRelatedSideEffects = True
			self.values['Pre-Session Headset-Related Side Effects'] = 'Yes'
			self.preSessionSideEffectsLayout()  # create the pre-session side-effects layout
			self.stacked_layout.addWidget(self.preSessionSideEffects_widget)  # add this to the stacked layout
			self.stacked_layout.setCurrentIndex(self.index)  # change the visible layout in the stack
			self.index += 1

	def preSessionSideEffectsLayout(self):
		if self.headsetRelatedSideEffects:
			label = 'Please select the side effect(s) that you experienced:'
		else:
			label = ''
		label_pre_session_side_effects = QtWidgets.QLabel(label)
		self.setFontStyle(label_pre_session_side_effects)

		if self.headsetRelatedSideEffects:
			checkBox_skinTingling = QtWidgets.QCheckBox('Skin tingling', self)
			checkBox_skinItching = QtWidgets.QCheckBox('Skin itching', self)
			checkBox_warmSensations = QtWidgets.QCheckBox('Sensations of warmth', self)
		checkBox_other = QtWidgets.QCheckBox('Report other side effects', self)

		preOtherSideEffects = QtWidgets.QLabel('')

		if self.headsetRelatedSideEffects:
			checkBoxes = [checkBox_skinTingling, checkBox_skinItching, checkBox_warmSensations, checkBox_other]
			preSideEffects = {checkBox_skinTingling: 'Skin tingling',
							  checkBox_skinItching: 'Skin itching',
							  checkBox_warmSensations: 'Sensations of warmth',
							  checkBox_other: 'Other'}
		else:
			checkBoxes = [checkBox_other]
			preSideEffects = {checkBox_other: 'Other'}

		for checkBox in checkBoxes:
			self.values['Intensity: Pre-Session ' + preSideEffects[checkBox]] = 0
			self.values['Duration: Pre-Session ' + preSideEffects[checkBox]] = 0

		self.values['Intensity: Pre-Session Other'] = []
		self.values['Duration: Pre-Session Other'] = []

		for checkBox in checkBoxes:
			self.setCheckBoxStyle(checkBox)

		if self.headsetRelatedSideEffects:
			checkBox_skinTingling.toggled.connect(lambda:self.preSessionSideEffectIntensity(checkBox_skinTingling, preSideEffects))
			checkBox_skinItching.toggled.connect(lambda:self.preSessionSideEffectIntensity(checkBox_skinItching, preSideEffects))
			checkBox_warmSensations.toggled.connect(lambda:self.preSessionSideEffectIntensity(checkBox_warmSensations, preSideEffects))
		checkBox_other.toggled.connect(lambda:self.preSessionOtherSideEffectIntensity(checkBox_other, preOtherSideEffects))

		# create a vertical layout to hold checkBoxes
		checkBox_layout = QtWidgets.QVBoxLayout()
		for checkBox in checkBoxes:
			checkBox_layout.addWidget(checkBox)

		button_back = QtWidgets.QPushButton('Back')
		button_next = QtWidgets.QPushButton('Next')

		buttons = [button_back, self.button_replay, button_next]
		button_layout = QtWidgets.QHBoxLayout()  # create a horizontal layout to hold buttons

		for button in buttons:
			self.setButtonStyle(button)
			button_layout.addWidget(button)

		# create a vertical layout to hold widgets
		preSessionSideEffects_layout = QtWidgets.QVBoxLayout()
		preSessionSideEffects_layout.addWidget(label_pre_session_side_effects)
		preSessionSideEffects_layout.addLayout(checkBox_layout)
		preSessionSideEffects_layout.addWidget(preOtherSideEffects)
		preSessionSideEffects_layout.addLayout(button_layout)

		# create a widget to display the layout
		self.preSessionSideEffects_widget = QtWidgets.QWidget()
		self.preSessionSideEffects_widget.setLayout(preSessionSideEffects_layout)

		# start the audio
		self.audioFile = self.audioPath + 'sideEffects_experienced.wav'
		self.buttonsToDisable = buttons
		if not self.isMute: self.playAudio()

		# button click connections
		button_back.clicked.connect(self.gotoPreviousWidget)
		button_next.clicked.connect(self.startPreSessionSideEffectsFreeTextLayout)

	def startPreSessionSideEffectsFreeTextLayout(self):
		global ongoingSpeech
		if not ongoingSpeech:
			if 'Intensity: Pre-Session Skin tingling' not in self.values:
				sideEffectsList = ['Skin tingling', 'Skin itching', 'Sensations of warmth']
				for sideEffect in sideEffectsList:
					self.values['Intensity: Pre-Session ' + sideEffect] = 0
					self.values['Duration: Pre-Session ' + sideEffect] = 0
			if 'Intensity: Pre-Session Other' not in self.values:
				self.values['Intensity: Pre-Session Other'] = []
				self.values['Duration: Pre-Session Other'] = []

			self.preSessionSideEffectsFreeTextLayout()  # create the pre-session other side effects layout
			self.stacked_layout.addWidget(self.preSessionOtherSideEffects_widget)  # add this to the stacked layout
			self.stacked_layout.setCurrentIndex(self.index)  # change the visible layout in the stack
			self.index += 1

	def preSessionSideEffectsFreeTextLayout(self):
		label = 'Are there any other side effects after your treatment ended that you would like to note?'
		label_otherSideEffects = QtWidgets.QLabel(label)
		self.setFontStyle(label_otherSideEffects)

		self.plainTextEdit_preSessionOtherSideEffects = QtWidgets.QPlainTextEdit()
		self.plainTextEdit_preSessionOtherSideEffects.resize(self.WIDTH * 0.08, self.HEIGHT * 0.15)
		self.setPlainTextEditStyle(self.plainTextEdit_preSessionOtherSideEffects)

		label = 'If none, please click \'Next\''
		label_noSideEffects = QtWidgets.QLabel(label)
		self.setFontStyle(label_noSideEffects)

		freeText_layout = QtWidgets.QVBoxLayout()
		freeText_layout.addWidget(label_otherSideEffects)
		freeText_layout.addWidget(self.plainTextEdit_preSessionOtherSideEffects)
		freeText_layout.addWidget(label_noSideEffects)
		freeText_layout.setContentsMargins(self.WIDTH * 0, self.HEIGHT * 0.10, self.WIDTH * 0, self.HEIGHT * 0.10)

		button_back = QtWidgets.QPushButton('Back')
		button_next = QtWidgets.QPushButton('Next')

		buttons = [button_back, self.button_replay, button_next]
		button_layout = QtWidgets.QHBoxLayout()  # create a horizontal layout to hold buttons

		for button in buttons:
			self.setButtonStyle(button)
			button_layout.addWidget(button)

		# create a vertical layout to hold widgets
		otherSideEffects_layout = QtWidgets.QVBoxLayout()
		otherSideEffects_layout.addLayout(freeText_layout)
		otherSideEffects_layout.addLayout(button_layout)

		# create a widget to display the layout
		self.preSessionOtherSideEffects_widget = QtWidgets.QWidget()
		self.preSessionOtherSideEffects_widget.setLayout(otherSideEffects_layout)

		# start the audio
		# self.audioFile = self.audioPath + '.wav'
		# self.buttonsToDisable = buttons
		# if not self.isMute: self.playAudio()

		# button click connections
		button_back.clicked.connect(self.gotoPreviousWidget)
		button_next.clicked.connect(self.startPreSessionDiseasePainLayout)

	def startPreSessionDiseasePainLayout(self):
		global ongoingSpeech
		if not ongoingSpeech:
			if self.preSessionSideEffects:
				self.values['Pre-Session Other Side Effects Text'] = self.plainTextEdit_preSessionOtherSideEffects.toPlainText()
			else:
				self.values['Pre-Session Other Side Effects Text'] = ''
				self.values['Pre-Session Headset-Related Side Effects'] = 'No'
			self.preSessionDiseasePainLayout()  # create the pre-session disease pain layout
			self.stacked_layout.addWidget(self.preSessionDiseasePain_widget)  # add this to the stacked layout
			self.stacked_layout.setCurrentIndex(self.index)  # change the visible layout in the stack
			self.index += 1

	def preSessionDiseasePainLayout(self):
		label = 'Do you have or feel any disease specific pain? Please indicate how much using the visual analog scale below.'
		label_pre_session_ms_pain = QtWidgets.QLabel(label)
		self.setFontStyle(label_pre_session_ms_pain)

		# add MS pain visual analogue scale image to QtWidgets.QLabel
		label_MS_pain = QtWidgets.QLabel(self)
		pixmap_MS_pain = QtGui.QPixmap('data/images/visual_MS_pain.jpg')
		label_MS_pain.setPixmap(pixmap_MS_pain.scaledToWidth(self.WIDTH * 0.4, QtCore.Qt.SmoothTransformation))

		self.radioButtonList_preMSPain = []
		radioButton_layout = QtWidgets.QHBoxLayout()
		radioButton_group = QtWidgets.QButtonGroup(self)
		radioButton_group.setExclusive(True)
		for i in range(11):
			radioButton = QtWidgets.QRadioButton(str(i))
			self.setRadioButtonStyle(radioButton)
			radioButton_group.addButton(radioButton, i)
			self.radioButtonList_preMSPain.append(radioButton)
			radioButton_layout.addWidget(radioButton)
			radioButton.toggled.connect(lambda:self.recordRadioButtonSelection(self.radioButtonList_preMSPain, 'Pre-Session MS pain'))
		self.setRadioButtonLayoutStyle(radioButton_layout)

		msPainScale_layout = QtWidgets.QVBoxLayout()
		msPainScale_layout.addWidget(label_MS_pain, QtCore.Qt.AlignCenter, QtCore.Qt.AlignCenter)
		msPainScale_layout.addLayout(radioButton_layout)
		self.setVisualAnalogScaleSpacing(msPainScale_layout)

		self.values['Pre-Session MS pain'] = 0

		button_back = QtWidgets.QPushButton('Back')
		button_next = QtWidgets.QPushButton('Next')

		buttons = [button_back, self.button_replay, button_next]
		button_layout = QtWidgets.QHBoxLayout()  # create a horizontal layout to hold buttons

		for button in buttons:
			self.setButtonStyle(button)
			button_layout.addWidget(button)

		# create a vertical layout to hold widgets
		preSessionDiseasePain_layout = QtWidgets.QVBoxLayout()
		preSessionDiseasePain_layout.addWidget(label_pre_session_ms_pain)
		preSessionDiseasePain_layout.addLayout(msPainScale_layout)
		preSessionDiseasePain_layout.addLayout(button_layout)

		# create a widget to display the layout
		self.preSessionDiseasePain_widget = QtWidgets.QWidget()
		self.preSessionDiseasePain_widget.setLayout(preSessionDiseasePain_layout)

		# start the audio
		self.audioFile = self.audioPath + 'disease_specific_pain.wav'
		self.buttonsToDisable = buttons
		if not self.isMute: self.playAudio()

		# button click connections
		button_back.clicked.connect(self.gotoPreviousWidget)
		button_next.clicked.connect(self.startPreSessionFatigueLayout)

	def startPreSessionFatigueLayout(self):
		global ongoingSpeech
		if not ongoingSpeech:
			selected = False
			for radioButton in self.radioButtonList_preMSPain:
				if radioButton.isChecked():
					selected = True
					break
			if not selected:
				QtWidgets.QMessageBox.critical(self, 'Disease specific pain',
					'Please enter the intensity of your disease specific pain before continuing further.', QtWidgets.QMessageBox.Ok)
			else:
				self.preSessionFatigueLayout()  # create the pre-session fatigue layout
				self.stacked_layout.addWidget(self.preSessionFatigue_widget)  # add this to the stacked layout
				self.stacked_layout.setCurrentIndex(self.index)  # change the visible layout in the stack
				self.index += 1

	def preSessionFatigueLayout(self):
		label = 'Please rate your current level of fatigue.'
		label_pre_session_fatigue = QtWidgets.QLabel(label)
		self.setFontStyle(label_pre_session_fatigue)

		# add MS pain visual analogue scale image to QtWidgets.QLabel
		label_fatigue = QtWidgets.QLabel(self)
		pixmap_fatigue = QtGui.QPixmap('data/images/visual_fatigue.jpg')
		label_fatigue.setPixmap(pixmap_fatigue.scaledToWidth(self.WIDTH * 0.4, QtCore.Qt.SmoothTransformation))

		self.radioButtonList_preFatigue = []
		radioButton_layout = QtWidgets.QHBoxLayout()
		radioButton_group = QtWidgets.QButtonGroup(self)
		radioButton_group.setExclusive(True)
		for i in range(11):
			radioButton = QtWidgets.QRadioButton(str(i))
			self.setRadioButtonStyle(radioButton)
			radioButton_group.addButton(radioButton, i)
			self.radioButtonList_preFatigue.append(radioButton)
			radioButton_layout.addWidget(radioButton)
			radioButton.toggled.connect(lambda:self.recordRadioButtonSelection(self.radioButtonList_preFatigue, 'Pre-Session Fatigue'))
		self.setRadioButtonLayoutStyle(radioButton_layout)

		fatigueScale_layout = QtWidgets.QVBoxLayout()
		fatigueScale_layout.addWidget(label_fatigue, QtCore.Qt.AlignCenter, QtCore.Qt.AlignCenter)
		fatigueScale_layout.addLayout(radioButton_layout)
		self.setVisualAnalogScaleSpacing(fatigueScale_layout)

		self.values['Pre-Session Fatigue'] = 0

		button_back = QtWidgets.QPushButton('Back')
		button_next = QtWidgets.QPushButton('Next')

		buttons = [button_back, self.button_replay, button_next]
		button_layout = QtWidgets.QHBoxLayout()  # create a horizontal layout to hold buttons

		for button in buttons:
			self.setButtonStyle(button)
			button_layout.addWidget(button)

		# create a vertical layout to hold widgets
		preSessionFatigue_layout = QtWidgets.QVBoxLayout()
		preSessionFatigue_layout.addWidget(label_pre_session_fatigue)
		preSessionFatigue_layout.addLayout(fatigueScale_layout)
		preSessionFatigue_layout.addLayout(button_layout)

		# create a widget to display the layout
		self.preSessionFatigue_widget = QtWidgets.QWidget()
		self.preSessionFatigue_widget.setLayout(preSessionFatigue_layout)

		# start the audio
		self.audioFile = self.audioPath + 'fatigue.wav'
		self.buttonsToDisable = buttons
		if not self.isMute: self.playAudio()

		# button click connections
		button_back.clicked.connect(self.gotoPreviousWidget)
		button_next.clicked.connect(self.startHoursSleptLayout)

	def startHoursSleptLayout(self):
		global ongoingSpeech
		if not ongoingSpeech:
			selected = False
			for radioButton in self.radioButtonList_preFatigue:
				if radioButton.isChecked():
					selected = True
					break
			if not selected:
				QtWidgets.QMessageBox.critical(self, 'Fatiuge',
					'Please enter the intensity of your fatigue before continuing further.', QtWidgets.QMessageBox.Ok)
			else:
				self.hoursSleptLayout()  # create the hours slept layout
				self.stacked_layout.addWidget(self.hoursSlept_widget)  # add this to the stacked layout
				self.stacked_layout.setCurrentIndex(self.index)  # change the visible layout in the stack
				self.index += 1

	def hoursSleptLayout(self):
		label1 = 'How many hours did you sleep last night?'
		label_sleep = QtWidgets.QLabel(label1)
		self.setFontStyle(label_sleep)

		validator = QtGui.QDoubleValidator()
		self.lineEdit_hoursSlept = QtWidgets.QLineEdit()
		self.lineEdit_hoursSlept.setAlignment(QtCore.Qt.AlignCenter)
		self.setLineEditStyle(self.lineEdit_hoursSlept)
		self.lineEdit_hoursSlept.setValidator(validator)

		hoursSlept_layout = QtWidgets.QVBoxLayout()
		hoursSlept_layout.addWidget(label_sleep)
		hoursSlept_layout.addWidget(self.lineEdit_hoursSlept)
		hoursSlept_layout.setAlignment(QtCore.Qt.AlignCenter)
		hoursSlept_layout.addStretch()

		label2 = 'How was your sleep last night?'
		label_sleepQuality = QtWidgets.QLabel(label2)
		self.setFontStyle(label_sleepQuality)

		self.dropDown_sleepQuality = QtWidgets.QComboBox()
		self.setComboBoxStyle(self.dropDown_sleepQuality, widthFactor=0.16)
		self.dropDown_sleepQuality.addItem('')
		self.dropDown_sleepQuality.addItem('About the same as usual')
		self.dropDown_sleepQuality.addItem('Better than usual')
		self.dropDown_sleepQuality.addItem('Worse than usual')
		self.dropDown_sleepQuality.currentIndexChanged.connect(self.sleepQuality)

		self.values['Sleep quality'] = ''

		sleepQuality_layout = QtWidgets.QVBoxLayout()
		sleepQuality_layout.addWidget(label_sleepQuality)
		sleepQuality_layout.addWidget(self.dropDown_sleepQuality)
		sleepQuality_layout.setAlignment(QtCore.Qt.AlignCenter)
		sleepQuality_layout.addStretch()

		label3 = 'When did you wake up today?'
		label_wakeUp = QtWidgets.QLabel(label3)
		self.setFontStyle(label_wakeUp)

		self.spinBox_wakeUpHours = QtWidgets.QSpinBox()
		self.spinBox_wakeUpHours.setRange(1, 12)
		self.spinBox_wakeUpHours.setValue(7)
		self.setSpinBoxStyle(self.spinBox_wakeUpHours)
		self.spinBox_wakeUpMins = QtWidgets.QSpinBox()
		self.spinBox_wakeUpMins.setRange(0, 59)
		self.setSpinBoxStyle(self.spinBox_wakeUpMins)
		self.dropDown_wakeUpAmPm = QtWidgets.QComboBox()
		self.setComboBoxStyle(self.dropDown_wakeUpAmPm)
		self.dropDown_wakeUpAmPm.setFixedWidth(self.WIDTH * 0.04)
		self.dropDown_wakeUpAmPm.addItem('AM')
		self.dropDown_wakeUpAmPm.addItem('PM')

		wakeUpTime_layout = QtWidgets.QHBoxLayout()
		wakeUpTime_layout.addWidget(self.spinBox_wakeUpHours)
		wakeUpTime_layout.addWidget(self.spinBox_wakeUpMins)
		wakeUpTime_layout.addWidget(self.dropDown_wakeUpAmPm)
		wakeUpTime_layout.addStretch()
		wakeUpTime_layout.setContentsMargins(self.WIDTH * 0.14, self.HEIGHT * 0, self.WIDTH * 0, self.HEIGHT * 0)
		wakeUpTime_layout.setAlignment(QtCore.Qt.AlignCenter)

		wakeUp_layout = QtWidgets.QVBoxLayout()
		wakeUp_layout.addWidget(label_wakeUp)
		wakeUp_layout.addLayout(wakeUpTime_layout)
		wakeUp_layout.setAlignment(QtCore.Qt.AlignCenter)
		wakeUp_layout.addStretch()

		button_back = QtWidgets.QPushButton('Back')
		button_next = QtWidgets.QPushButton('Next')

		buttons = [button_back, self.button_replay, button_next]
		button_layout = QtWidgets.QHBoxLayout()  # create a horizontal layout to hold buttons

		for button in buttons:
			self.setButtonStyle(button)
			button_layout.addWidget(button)

		# create a vertical layout to hold widgets
		sleepDetails_layout = QtWidgets.QVBoxLayout()
		sleepDetails_layout.addLayout(hoursSlept_layout)
		sleepDetails_layout.addLayout(sleepQuality_layout)
		sleepDetails_layout.addLayout(wakeUp_layout)
		sleepDetails_layout.addLayout(button_layout)
		sleepDetails_layout.setContentsMargins(self.WIDTH * 0.00573, self.HEIGHT * 0.07, self.WIDTH * 0.00573, self.HEIGHT * 0.01018)

		# create a widget to display the layout
		self.hoursSlept_widget = QtWidgets.QWidget()
		self.hoursSlept_widget.setLayout(sleepDetails_layout)

		# start the audio
		self.audioFile = self.audioPath + 'sleep.wav'
		self.buttonsToDisable = buttons
		if not self.isMute: self.playAudio()

		# button click connections
		button_back.clicked.connect(self.gotoPreviousWidget)
		button_next.clicked.connect(self.startPreSessionPanasQuestionnaireLayout)

	def startPreSessionPanasQuestionnaireLayout(self):
		global ongoingSpeech
		if not ongoingSpeech:
			if self.lineEdit_hoursSlept.text().strip() == '':
				QtWidgets.QMessageBox.critical(self, 'Hours Slept',
					'Please enter the number of hours you have slept before continuing further.', QtWidgets.QMessageBox.Ok)
			elif self.values['Sleep quality'] == '':
				QtWidgets.QMessageBox.critical(self, 'Sleep Quality',
					'Please rate your last night\'s sleep before continuing further.', QtWidgets.QMessageBox.Ok)
			else:
				self.values['Hours slept'] = self.lineEdit_hoursSlept.text()
				wakeUpTimeHours = int(self.spinBox_wakeUpHours.value())
				wakeUpTimeMins = int(self.spinBox_wakeUpMins.value())
				wakeUpTimeAmPm = self.dropDown_wakeUpAmPm.currentText()
				if wakeUpTimeAmPm == 'PM' and wakeUpTimeHours < 12:
					self.values['Wake up time'] = str(wakeUpTimeHours + 12) + ':' + str(wakeUpTimeMins)
				elif wakeUpTimeAmPm == 'AM' and wakeUpTimeHours == 12:
					self.values['Wake up time'] = str(wakeUpTimeHours - 12) + ':' + str(wakeUpTimeMins)
				else:
					self.values['Wake up time'] = str(wakeUpTimeHours) + ':' + str(wakeUpTimeMins)
				self.preSessionPanasQuestionnaireLayout()  # create the PANAS questionnaire layout
				self.stacked_layout.addWidget(self.preSessionPanasQuestionnaire_widget)  # add this to the stacked layout
				self.stacked_layout.setCurrentIndex(self.index)  # change the visible layout in the stack
				self.index += 1

	def preSessionPanasQuestionnaireLayout(self):
		label = 'Please indicate to what extent you are feeling this way right now.'
		label_panas = QtWidgets.QLabel(label)
		self.setFontStyle(label_panas)

		N_ROWS, N_COLS = 20, 5

		self.preSessionPanasTable_widget = QtWidgets.QTableWidget()
		self.preSessionPanasTable_widget.setRowCount(N_ROWS)
		self.preSessionPanasTable_widget.setColumnCount(N_COLS)
		self.setTableStyle(self.preSessionPanasTable_widget)

		panas_col_headers = ['Very slightly or not at all', 'A little', 'Moderately', 'Quite a bit', 'Extremely']
		self.preSessionPanasTable_widget.setHorizontalHeaderLabels(panas_col_headers)

		panas_permutations = [['Interested', 'Distressed', 'Excited', 'Upset', 'Strong', 'Guilty', 'Scared', 'Hostile', 'Enthusiastic', 'Proud',
							   'Irritable', 'Alert', 'Ashamed', 'Inspired', 'Nervous', 'Determined', 'Attentive', 'Jittery', 'Active', 'Afraid'],
							  ['Active', 'Irritable', 'Strong', 'Ashamed', 'Inspired', 'Nervous', 'Jittery', 'Afraid', 'Excited', 'Determined',
							   'Distressed', 'Interested', 'Upset', 'Enthusiastic', 'Guilty', 'Proud', 'Alert', 'Scared', 'Attentive', 'Hostile'],
							  ['Inspired', 'Scared', 'Active', 'Jittery', 'Excited', 'Irritable', 'Distressed', 'Nervous', 'Strong', 'Interested',
							   'Ashamed', 'Determined', 'Afraid', 'Proud', 'Hostile', 'Enthusiastic', 'Attentive', 'Guilty', 'Alert', 'Upset'],
							  ['Excited', 'Hostile', 'Attentive', 'Scared', 'Active', 'Distressed', 'Irritable', 'Jittery', 'Inspired', 'Strong',
							   'Nervous', 'Proud', 'Afraid', 'Alert', 'Ashamed', 'Interested', 'Enthusiastic', 'Upset', 'Determined', 'Guilty']]

		if 'Session number' not in self.values:
			self.values['Session number'] = 1 if len(self.user_data) == 0 else self.user_data['Session number'].max() + 1

		self.panas_row_headers = panas_permutations[(int(self.values['Session number'])%4)-1][:]
		self.preSessionPanasTable_widget.setVerticalHeaderLabels(self.panas_row_headers)

		self.panas_buttons = [[None] * N_COLS for _ in range(N_ROWS)]

		for r in range(N_ROWS):
			rating_button_group = QtWidgets.QButtonGroup(self)
			rating_button_group.setExclusive(True)
			for c in range(N_COLS):
				radio_button = QtWidgets.QRadioButton(str(c+1))
				self.preSessionPanasTable_widget.setCellWidget(r, c, radio_button)
				rating_button_group.addButton(radio_button, c)
				self.panas_buttons[r][c] = radio_button

		header = self.preSessionPanasTable_widget.horizontalHeader()
		header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
		header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
		header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
		header.setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)
		header.setSectionResizeMode(4, QtWidgets.QHeaderView.Stretch)

		self.preSessionPanasTable_widget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)  # disable editing of content
		self.preSessionPanasTable_widget.setWordWrap(True)

		button_back = QtWidgets.QPushButton('Back')
		button_next = QtWidgets.QPushButton('Next')

		buttons = [button_back, self.button_replay, button_next]
		button_layout = QtWidgets.QHBoxLayout()  # create a horizontal layout to hold buttons

		for button in buttons:
			self.setButtonStyle(button)
			button_layout.addWidget(button)

		# create a vertical layout to hold widgets
		panasQuestionnaire_layout = QtWidgets.QVBoxLayout()
		panasQuestionnaire_layout.addWidget(label_panas)
		panasQuestionnaire_layout.addWidget(self.preSessionPanasTable_widget)
		panasQuestionnaire_layout.addLayout(button_layout)

		# create a widget to display the layout
		self.preSessionPanasQuestionnaire_widget = QtWidgets.QWidget()
		self.preSessionPanasQuestionnaire_widget.setLayout(panasQuestionnaire_layout)

		# start the audio
		self.audioFile = self.audioPath + 'panas.wav'
		self.buttonsToDisable = buttons
		if not self.isMute: self.playAudio()

		# button click connections
		button_back.clicked.connect(self.gotoPreviousWidget)
		button_next.clicked.connect(self.startContactQualityLayout)

	def startContactQualityLayout(self):
		global ongoingSpeech
		if not ongoingSpeech:
			count_selected = 0
			for r, buttons in enumerate(self.panas_buttons):
				selected = False
				for c, button in enumerate(buttons):
					if button.isChecked():
						selected = True
						count_selected += 1
						self.values['Pre-Session PANAS: ' + self.panas_row_headers[r]] = c+1
				if not selected:
					self.setTableRowBackgroundColor(self.preSessionPanasTable_widget, r, '#FFFF00')
				else:
					self.setTableRowBackgroundColor(self.preSessionPanasTable_widget, r, '#FFFFFF')

			if count_selected == len(self.panas_row_headers):
				self.contactQualityLayout()  # create the contact quality layout
				self.stacked_layout.addWidget(self.contactQuality_widget)  # add this to the stacked layout
				self.stacked_layout.setCurrentIndex(self.index)  # change the visible layout in the stack
				self.index += 1
			else:
				QtWidgets.QMessageBox.critical(self, 'Incomplete answers',
					'Please select values for all parameters before continuing further.', QtWidgets.QMessageBox.Ok)

	def contactQualityLayout(self):
		label1 = 'Please enter the contact quality displayed on your tDCS device'
		label1_contactQuality = QtWidgets.QLabel(label1)
		self.setFontStyle(label1_contactQuality)

		qualityTypes = ['Good', 'Moderate', 'Poor']
		self.dropDown_contactQuality = QtWidgets.QComboBox()
		self.setComboBoxStyle(self.dropDown_contactQuality)
		for qualityType in qualityTypes:
			self.dropDown_contactQuality.addItem(qualityType)
		self.dropDown_contactQuality.currentIndexChanged.connect(self.contactQuality)

		self.values['Contact quality'] = 'Good'

		dropDown_layout = QtWidgets.QHBoxLayout()
		dropDown_layout.addWidget(self.dropDown_contactQuality)
		dropDown_layout.setContentsMargins(self.WIDTH * 0, self.HEIGHT * 0.05, self.WIDTH * 0, self.HEIGHT * 0.15)

		label2 = 'If contact quality is poor, check the following: \n \
		Is there any hair obstructing the sponge-skin contact? \n \
		Are the sponges in the correct position? \n \
		Are the electrodes snapped in all the way? \n \
		Are the headset wires plugged into the device? \n \
		Are the sponges completely dried out?'

		label2_contactQuality = QtWidgets.QLabel(label2)
		self.setFontStyle(label2_contactQuality, size=15)

		button_back = QtWidgets.QPushButton('Back')
		button_next = QtWidgets.QPushButton('Next')

		buttons = [button_back, self.button_replay, button_next]
		button_layout = QtWidgets.QHBoxLayout()  # create a horizontal layout to hold buttons

		for button in buttons:
			self.setButtonStyle(button)
			button_layout.addWidget(button)

		button_layout.setContentsMargins(self.WIDTH * 0, self.HEIGHT * 0.05, self.WIDTH * 0, self.HEIGHT * 0)

		# create a vertical layout to hold widgets
		contactQuality_layout = QtWidgets.QVBoxLayout()
		contactQuality_layout.addWidget(label1_contactQuality)
		contactQuality_layout.addLayout(dropDown_layout)
		contactQuality_layout.addWidget(label2_contactQuality)
		contactQuality_layout.addLayout(button_layout)

		# create a widget to display the layout
		self.contactQuality_widget = QtWidgets.QWidget()
		self.contactQuality_widget.setLayout(contactQuality_layout)

		# start the audio
		self.audioFile = self.audioPath + 'contact_quality.wav'
		self.buttonsToDisable = buttons
		if not self.isMute: self.playAudio()

		# button click connections
		button_back.clicked.connect(self.gotoPreviousWidget)
		button_next.clicked.connect(self.startDoseCodeLayout)

	def startDoseCodeLayout(self):
		global ongoingSpeech
		if not ongoingSpeech:
			self.doseCodeLayout()  # create the dose code layout
			self.stacked_layout.addWidget(self.doseCode_widget)  # add this to the stacked layout
			self.stacked_layout.setCurrentIndex(self.index)  # change the visible layout in the stack
			self.index += 1

	def doseCodeLayout(self):
		label = 'Please enter the dose code that you have been provided'
		label_dose_code = QtWidgets.QLabel(label)
		self.setFontStyle(label_dose_code)

		self.lineEdit_dose_code = QtWidgets.QLineEdit()
		self.lineEdit_dose_code.setAlignment(QtCore.Qt.AlignCenter)
		self.setLineEditStyle(self.lineEdit_dose_code)

		button_back = QtWidgets.QPushButton('Back')
		button_next = QtWidgets.QPushButton('Next')

		buttons = [button_back, self.button_replay, button_next]
		button_layout = QtWidgets.QHBoxLayout()  # create a horizontal layout to hold buttons

		for button in buttons:
			self.setButtonStyle(button)
			button_layout.addWidget(button)

		button_layout.setContentsMargins(self.WIDTH * 0, self.HEIGHT * 0.25, self.WIDTH * 0, self.HEIGHT * 0)

		# create a vertical layout to hold widgets
		doseCode_layout = QtWidgets.QVBoxLayout()
		doseCode_layout.addWidget(label_dose_code, QtCore.Qt.AlignCenter, QtCore.Qt.AlignCenter)
		doseCode_layout.addWidget(self.lineEdit_dose_code, QtCore.Qt.AlignCenter, QtCore.Qt.AlignCenter)
		doseCode_layout.addLayout(button_layout)
		doseCode_layout.setContentsMargins(self.WIDTH * 0.00573, self.HEIGHT * 0.1, self.WIDTH * 0.00573, self.HEIGHT * 0.01018)

		# create a widget to display the layout
		self.doseCode_widget = QtWidgets.QWidget()
		self.doseCode_widget.setLayout(doseCode_layout)

		# start the audio
		self.audioFile = self.audioPath + 'dose_code.wav'
		self.buttonsToDisable = buttons
		if not self.isMute: self.playAudio()

		# button click connections
		button_back.clicked.connect(self.gotoPreviousWidget)
		button_next.clicked.connect(self.startTrainingLayout)

	def startTrainingLayout(self):
		global ongoingSpeech
		if not ongoingSpeech:
			user_dose_code = self.lineEdit_dose_code.text()
			user_dose_code = user_dose_code.strip().replace(' ','')
			# if user_dose_code == self.dose_current_session:
			if user_dose_code != '':
				now = datetime.now()
				FMT = '%H:%M'
				self.values['Date'] = now.strftime('%Y-%m-%d')
				self.values['Start time'] = now.strftime(FMT)
				self.values['Dose code'] = user_dose_code
				self.values['Time since woke up'] = datetime.strptime(self.values['Start time'], FMT) - datetime.strptime(self.values['Wake up time'], FMT)
				self.trainingLayout()  # create the training layout
				self.stacked_layout.addWidget(self.training_widget)  # add this to the stacked layout
				self.stacked_layout.setCurrentIndex(self.index)  # change the visible layout in the stack
				self.index += 1
				self.showProgress()  # show the progress of stimulation time
			# else:
			# 	QtWidgets.QMessageBox.critical(self, 'Incorrect code',
			# 		'You have entered an incorrect dose code. Please try again with a valid dose code.', QtWidgets.QMessageBox.Ok)
			else:
				QtWidgets.QMessageBox.critical(self, 'Invalid code',
					'Please enter the dose code before continuing further', QtWidgets.QMessageBox.Ok)

	def trainingLayout(self):
		self.removeWindowOnTopFlag()

		self.startTime = int(time.time())

		label1 = 'Your stimulation has begun and your training program is being loaded...'
		label_training = QtWidgets.QLabel(label1)
		self.setFontStyle(label_training)

		self.progressBar_passedTime = QtWidgets.QProgressBar(self)
		self.setProgressBarStyle(self.progressBar_passedTime)

		# add caution image to QtWidgets.QLabel
		label_caution = QtWidgets.QLabel(self)
		pixmap_caution = QtGui.QPixmap('data/images/caution.png')
		label_caution.setPixmap(pixmap_caution.scaledToWidth(self.WIDTH * 0.05, QtCore.Qt.SmoothTransformation))

		label2 = 'Please do not close this application while the tDCS session is underway.'
		label_warning = QtWidgets.QLabel(label2)
		self.setFontStyle(label_warning)
		label_warning.setFont(QtGui.QFont('Calibri', 15, weight=QtGui.QFont.Bold))

		warning_layout = QtWidgets.QVBoxLayout()
		warning_layout.addWidget(label_caution, 0, QtCore.Qt.AlignCenter)
		warning_layout.addWidget(label_warning)
		warning_layout.setContentsMargins(self.WIDTH * 0, self.HEIGHT * 0.10, self.WIDTH * 0, self.HEIGHT * 0.10)

		button_help = QtWidgets.QPushButton('Help')
		buttons = [button_help]
		button_layout = QtWidgets.QHBoxLayout()  # create a horizontal layout to hold buttons

		for button in buttons:
			self.setButtonStyle(button)
			button_layout.addWidget(button)

		# create a vertical layout to hold widgets
		training_layout = QtWidgets.QVBoxLayout()
		training_layout.addWidget(label_training)
		training_layout.addWidget(self.progressBar_passedTime)
		training_layout.addLayout(warning_layout)
		training_layout.addLayout(button_layout)

		# create a widget to display the layout
		self.training_widget = QtWidgets.QWidget()
		self.training_widget.setLayout(training_layout)

		# start the audio
		self.audioFile = self.audioPath + 'stimulation_begin.wav'
		self.buttonsToDisable = buttons
		if not self.isMute: self.playAudio()

		# button click connections
		button_help.clicked.connect(lambda:self.help(self.studyID))

	def startStimulationEndedLayout(self):
		global ongoingSpeech
		if not ongoingSpeech:
			self.values['End time'] = datetime.now().strftime('%H:%M')
			self.stimulationEndedLayout()  # create the stimulation ended layout
			self.stacked_layout.addWidget(self.stimulationEnded_widget)  # add this to the stacked layout
			self.stacked_layout.setCurrentIndex(self.index)  # change the visible layout in the stack
			self.index += 1

	def stimulationEndedLayout(self):
		self.addWindowOnTopFlag()

		label1 = 'Your stimulation session has ended and you may remove the headset.'
		label_stimulationEnded = QtWidgets.QLabel(label1)
		self.setFontStyle(label_stimulationEnded)

		label2 = 'Press any key on the device to shut it down.'
		label_shutDown = QtWidgets.QLabel(label2)
		self.setFontStyle(label_shutDown)

		label3 = 'Please complete the following questions.'
		label_completeQuestions = QtWidgets.QLabel(label3)
		self.setFontStyle(label_completeQuestions)

		button_next = QtWidgets.QPushButton('Next')

		buttons = [self.button_replay, button_next]
		button_layout = QtWidgets.QHBoxLayout()  # create a horizontal layout to hold buttons

		for button in buttons:
			self.setButtonStyle(button)
			button_layout.addWidget(button)

		# create a vertical layout to hold widgets
		stimulationEnded_layout = QtWidgets.QVBoxLayout()
		stimulationEnded_layout.addWidget(label_stimulationEnded)
		stimulationEnded_layout.addWidget(label_shutDown)
		stimulationEnded_layout.addWidget(label_completeQuestions)
		stimulationEnded_layout.addLayout(button_layout)

		# create a widget to display the layout
		self.stimulationEnded_widget = QtWidgets.QWidget()
		self.stimulationEnded_widget.setLayout(stimulationEnded_layout)

		# start the audio
		self.audioFile = self.audioPath + 'stimulation_ended.wav'
		self.buttonsToDisable = buttons
		if not self.isMute: self.playAudio()

		# button click connections
		button_next.clicked.connect(self.startPostSessionHeadsetPainLayout)

	def startPostSessionHeadsetPainLayout(self):
		global ongoingSpeech
		if not ongoingSpeech:
			self.postSessionHeadsetPainLayout()  # create the post-session headset pain layout
			self.stacked_layout.addWidget(self.postSessionHeadsetPain_widget)  # add this to the stacked layout
			self.stacked_layout.setCurrentIndex(self.index)  # change the visible layout in the stack
			self.index += 1

	def postSessionHeadsetPainLayout(self):
		label = 'Do you feel pain from the headset? Please enter the intensity of your pain.'
		label_headset_pain = QtWidgets.QLabel(label)
		self.setFontStyle(label_headset_pain)

		# add headset pain visual analogue scale image to QtWidgets.QLabel
		visual_headset_pain = QtWidgets.QLabel(self)
		pixmap_headset_pain = QtGui.QPixmap('data/images/visual_MS_pain.jpg')
		visual_headset_pain.setPixmap(pixmap_headset_pain.scaledToWidth(self.WIDTH * 0.4, QtCore.Qt.SmoothTransformation))

		self.radioButtonList_postHeadsetPain = []
		radioButton_layout = QtWidgets.QHBoxLayout()
		radioButton_group = QtWidgets.QButtonGroup(self)
		radioButton_group.setExclusive(True)
		for i in range(11):
			radioButton = QtWidgets.QRadioButton(str(i))
			self.setRadioButtonStyle(radioButton)
			radioButton_group.addButton(radioButton, i)
			self.radioButtonList_postHeadsetPain.append(radioButton)
			radioButton_layout.addWidget(radioButton)
			radioButton.toggled.connect(lambda:self.recordRadioButtonSelection(self.radioButtonList_postHeadsetPain, 'Post-Session Headset Device Pain'))
		self.setRadioButtonLayoutStyle(radioButton_layout)

		headsetPainScale_layout = QtWidgets.QVBoxLayout()
		headsetPainScale_layout.addWidget(visual_headset_pain, QtCore.Qt.AlignCenter, QtCore.Qt.AlignCenter)
		headsetPainScale_layout.addLayout(radioButton_layout)
		self.setVisualAnalogScaleSpacing(headsetPainScale_layout)

		self.values['Post-Session Headset Device Pain'] = 0

		button_back = QtWidgets.QPushButton('Back')
		button_next = QtWidgets.QPushButton('Next')

		buttons = [button_back, self.button_replay, button_next]
		button_layout = QtWidgets.QHBoxLayout()  # create a horizontal layout to hold buttons

		for button in buttons:
			self.setButtonStyle(button)
			button_layout.addWidget(button)

		# create a vertical layout to hold widgets
		postSessionHeadsetPain_layout = QtWidgets.QVBoxLayout()
		postSessionHeadsetPain_layout.addWidget(label_headset_pain)
		postSessionHeadsetPain_layout.addLayout(headsetPainScale_layout)
		postSessionHeadsetPain_layout.addLayout(button_layout)

		# create a widget to display the layout
		self.postSessionHeadsetPain_widget = QtWidgets.QWidget()
		self.postSessionHeadsetPain_widget.setLayout(postSessionHeadsetPain_layout)

		# start the audio
		self.audioFile = self.audioPath + 'headset_pain.wav'
		self.buttonsToDisable = buttons
		if not self.isMute: self.playAudio()

		# button click connections
		button_back.clicked.connect(self.gotoPreviousWidget)
		button_next.clicked.connect(self.startPostSessionSideEffectsExperiencedLayout)

	def startPostSessionSideEffectsExperiencedLayout(self):
		global ongoingSpeech
		if not ongoingSpeech:
			selected = False
			for radioButton in self.radioButtonList_postHeadsetPain:
				if radioButton.isChecked():
					selected = True
					break
			if not selected:
				QtWidgets.QMessageBox.critical(self, 'Pain from headset',
					'Please enter the intensity of your pain from the headset before continuing further.', QtWidgets.QMessageBox.Ok)
			else:
				if 'Post-Session Headset Device Pain' not in self.values:
					self.values['Post-Session Headset Device Pain'] = 0
				if int(self.values['Post-Session Headset Device Pain']) >= self.PAIN_THRESHOLD:
					self.highPain(self.studyID)
				self.postSessionSideEffectsExperiencedLayout()  # create the post-session side-effects experienced layout
				self.stacked_layout.addWidget(self.postSessionSideEffectsExperienced_widget)  # add this to the stacked layout
				self.stacked_layout.setCurrentIndex(self.index)  # change the visible layout in the stack
				self.index += 1

	def postSessionSideEffectsExperiencedLayout(self):
		self.postSessionSideEffects = True
		label = 'Did you feel any side effect(s) during this tDCS session?'
		label_post_session_side_effects_experienced = QtWidgets.QLabel(label)
		self.setFontStyle(label_post_session_side_effects_experienced)

		button_back = QtWidgets.QPushButton('Back')
		button_no = QtWidgets.QPushButton('No')
		button_yes = QtWidgets.QPushButton('Yes')

		buttons = [button_back, self.button_replay, button_no, button_yes]
		button_layout = QtWidgets.QHBoxLayout()  # create a horizontal layout to hold buttons

		for button in buttons:
			self.setButtonStyle(button)
			button_layout.addWidget(button)

		# create a vertical layout to hold widgets
		postSessionSideEffectsExperienced_layout = QtWidgets.QVBoxLayout()
		postSessionSideEffectsExperienced_layout.addWidget(label_post_session_side_effects_experienced)
		postSessionSideEffectsExperienced_layout.addLayout(button_layout)

		# create a widget to display the layout
		self.postSessionSideEffectsExperienced_widget = QtWidgets.QWidget()
		self.postSessionSideEffectsExperienced_widget.setLayout(postSessionSideEffectsExperienced_layout)

		# start the audio
		self.audioFile = self.audioPath + 'sideEffects_currentSession.wav'
		self.buttonsToDisable = buttons
		if not self.isMute: self.playAudio()

		# button click connections
		button_back.clicked.connect(self.gotoPreviousWidget)
		button_no.clicked.connect(self.postSessionNoSideEffects)
		button_yes.clicked.connect(self.startPostSessionSideEffectsHeadsetRelatedLayout)

	def postSessionNoSideEffects(self):
		global ongoingSpeech
		if not ongoingSpeech:
			self.postSessionSideEffects = False
			sideEffects = ['Skin tingling', 'Skin itching', 'Sensations of warmth']
			for sideEffect in sideEffects:
				self.values['Intensity: Post-Session ' + sideEffect] = 0
				self.values['Duration: Post-Session ' + sideEffect] = 0
			self.values['Intensity: Post-Session Other'] = []
			self.values['Duration: Post-Session Other'] = []
			self.startPostSessionDiseasePainLayout()

	def startPostSessionSideEffectsHeadsetRelatedLayout(self):
		global ongoingSpeech
		if not ongoingSpeech:
			self.postSessionSideEffectsHeadsetRelatedLayout()  # create the post-session headset related side-effects layout
			self.stacked_layout.addWidget(self.postSessionSideEffectsHeadset_widget)  # add this to the stacked layout
			self.stacked_layout.setCurrentIndex(self.index)  # change the visible layout in the stack
			self.index += 1

	def postSessionSideEffectsHeadsetRelatedLayout(self):
		# these values will be changed if they click 'No'
		self.headsetRelatedSideEffects = True
		self.values['Post-Session Headset-Related Side Effects'] = 'Yes'

		label = 'Were any of the side effects related to the headset?'
		label_post_session_side_effects_headset = QtWidgets.QLabel(label)
		self.setFontStyle(label_post_session_side_effects_headset)

		button_back = QtWidgets.QPushButton('Back')
		button_no = QtWidgets.QPushButton('No')
		button_yes = QtWidgets.QPushButton('Yes')

		buttons = [button_back, self.button_replay, button_no, button_yes]
		button_layout = QtWidgets.QHBoxLayout()  # create a horizontal layout to hold buttons

		for button in buttons:
			self.setButtonStyle(button)
			button_layout.addWidget(button)

		# create a vertical layout to hold widgets
		postSessionSideEffectsHeadset_layout = QtWidgets.QVBoxLayout()
		postSessionSideEffectsHeadset_layout.addWidget(label_post_session_side_effects_headset)
		postSessionSideEffectsHeadset_layout.addLayout(button_layout)

		# create a widget to display the layout
		self.postSessionSideEffectsHeadset_widget = QtWidgets.QWidget()
		self.postSessionSideEffectsHeadset_widget.setLayout(postSessionSideEffectsHeadset_layout)

		# start the audio
		# self.audioFile = self.audioPath + '.wav'
		# self.buttonsToDisable = buttons
		# if not self.isMute: self.playAudio()

		# button click connections
		button_back.clicked.connect(self.gotoPreviousWidget)
		button_no.clicked.connect(self.postSessionNoHeadsetRelatedSideEffects)
		button_yes.clicked.connect(self.startPostSessionSideEffectsLayout)

	def postSessionNoHeadsetRelatedSideEffects(self):
		global ongoingSpeech
		if not ongoingSpeech:
			self.headsetRelatedSideEffects = False
			self.values['Post-Session Headset-Related Side Effects'] = 'No'
			sideEffects = ['Skin tingling', 'Skin itching', 'Sensations of warmth']
			for sideEffect in sideEffects:
				self.values['Intensity: Post-Session ' + sideEffect] = 0
				self.values['Duration: Post-Session ' + sideEffect] = 0
			self.postSessionSideEffectsLayout()  # create the post-session side-effects layout
			self.stacked_layout.addWidget(self.postSessionSideEffects_widget)  # add this to the stacked layout
			self.stacked_layout.setCurrentIndex(self.index)  # change the visible layout in the stack
			self.index += 1

	def startPostSessionSideEffectsLayout(self):
		global ongoingSpeech
		if not ongoingSpeech:
			self.headsetRelatedSideEffects = True
			self.values['Post-Session Headset-Related Side Effects'] = 'Yes'
			self.postSessionSideEffectsLayout()  # create the post-session side-effects layout
			self.stacked_layout.addWidget(self.postSessionSideEffects_widget)  # add this to the stacked layout
			self.stacked_layout.setCurrentIndex(self.index)  # change the visible layout in the stack
			self.index += 1

	def postSessionSideEffectsLayout(self):
		if self.headsetRelatedSideEffects:
			label = 'Please select the side effect(s) that you experienced:'
		else:
			label = ''
		label_post_session_side_effects = QtWidgets.QLabel(label)
		self.setFontStyle(label_post_session_side_effects)

		if self.headsetRelatedSideEffects:
			checkBox_skinTingling = QtWidgets.QCheckBox('Skin tingling', self)
			checkBox_skinItching = QtWidgets.QCheckBox('Skin itching', self)
			checkBox_warmSensations = QtWidgets.QCheckBox('Sensations of warmth', self)
		checkBox_other = QtWidgets.QCheckBox('Report other side effects', self)

		postOtherSideEffects = QtWidgets.QLabel('')

		if self.headsetRelatedSideEffects:
			checkBoxes = [checkBox_skinTingling, checkBox_skinItching, checkBox_warmSensations, checkBox_other]
			postSideEffects = {checkBox_skinTingling:'Skin tingling',
							   checkBox_skinItching: 'Skin itching',
							   checkBox_warmSensations: 'Sensations of warmth',
							   checkBox_other: 'Other'}
		else:
			checkBoxes = [checkBox_other]
			postSideEffects = {checkBox_other: 'Other'}

		for checkBox in checkBoxes:
			self.values['Intensity: Post-Session ' + postSideEffects[checkBox]] = 0
			self.values['Duration: Post-Session ' + postSideEffects[checkBox]] = 0

		self.values['Intensity: Post-Session Other'] = []
		self.values['Duration: Post-Session Other'] = []

		for checkBox in checkBoxes:
			self.setCheckBoxStyle(checkBox)

		if self.headsetRelatedSideEffects:
			checkBox_skinTingling.toggled.connect(lambda:self.postSessionSideEffectIntensity(checkBox_skinTingling, postSideEffects))
			checkBox_skinItching.toggled.connect(lambda:self.postSessionSideEffectIntensity(checkBox_skinItching, postSideEffects))
			checkBox_warmSensations.toggled.connect(lambda:self.postSessionSideEffectIntensity(checkBox_warmSensations, postSideEffects))
		checkBox_other.toggled.connect(lambda:self.postSessionOtherSideEffectIntensity(checkBox_other, postOtherSideEffects))

		# create a vertical layout to hold checkBoxes
		checkBox_layout = QtWidgets.QVBoxLayout()
		for checkBox in checkBoxes:
			checkBox_layout.addWidget(checkBox)

		button_back = QtWidgets.QPushButton('Back')
		button_next = QtWidgets.QPushButton('Next')

		buttons = [button_back, self.button_replay, button_next]
		button_layout = QtWidgets.QHBoxLayout()  # create a horizontal layout to hold buttons

		for button in buttons:
			self.setButtonStyle(button)
			button_layout.addWidget(button)

		# create a vertical layout to hold widgets
		postSessionSideEffects_layout = QtWidgets.QVBoxLayout()
		postSessionSideEffects_layout.addWidget(label_post_session_side_effects)
		postSessionSideEffects_layout.addLayout(checkBox_layout)
		postSessionSideEffects_layout.addWidget(postOtherSideEffects)
		postSessionSideEffects_layout.addLayout(button_layout)

		# create a widget to display the layout
		self.postSessionSideEffects_widget = QtWidgets.QWidget()
		self.postSessionSideEffects_widget.setLayout(postSessionSideEffects_layout)

		# start the audio
		self.audioFile = self.audioPath + 'sideEffects_experienced.wav'
		self.buttonsToDisable = buttons
		if not self.isMute: self.playAudio()

		# button click connections
		button_back.clicked.connect(self.gotoPreviousWidget)
		button_next.clicked.connect(self.startPostSessionSideEffectsFreeTextLayout)

	def startPostSessionSideEffectsFreeTextLayout(self):
		global ongoingSpeech
		if not ongoingSpeech:
			if 'Intensity: Post-Session Skin tingling' not in self.values:
				sideEffectsList = ['Skin tingling', 'Skin itching', 'Sensations of warmth']
				for sideEffect in sideEffectsList:
					self.values['Intensity: Post-Session ' + sideEffect] = 0
					self.values['Duration: Post-Session ' + sideEffect] = 0
			if 'Intensity: Post-Session Other' not in self.values:
				self.values['Intensity: Post-Session Other'] = []
				self.values['Duration: Post-Session Other'] = []

			self.postSessionSideEffectsFreeTextLayout()  # create the post-session other side effects layout
			self.stacked_layout.addWidget(self.postSessionOtherSideEffects_widget)  # add this to the stacked layout
			self.stacked_layout.setCurrentIndex(self.index)  # change the visible layout in the stack
			self.index += 1

	def postSessionSideEffectsFreeTextLayout(self):
		label = 'Are there any other side effects after your treatment ended that you would like to note?'
		label_otherSideEffects = QtWidgets.QLabel(label)
		self.setFontStyle(label_otherSideEffects)

		self.plainTextEdit_postSessionOtherSideEffects = QtWidgets.QPlainTextEdit()
		self.plainTextEdit_postSessionOtherSideEffects.resize(self.WIDTH * 0.08, self.HEIGHT * 0.15)
		self.setPlainTextEditStyle(self.plainTextEdit_postSessionOtherSideEffects)

		label = 'If none, please click \'Next\''
		label_noSideEffects = QtWidgets.QLabel(label)
		self.setFontStyle(label_noSideEffects)

		freeText_layout = QtWidgets.QVBoxLayout()
		freeText_layout.addWidget(label_otherSideEffects)
		freeText_layout.addWidget(self.plainTextEdit_postSessionOtherSideEffects)
		freeText_layout.addWidget(label_noSideEffects)
		freeText_layout.setContentsMargins(self.WIDTH * 0, self.HEIGHT * 0.10, self.WIDTH * 0, self.HEIGHT * 0.10)

		button_back = QtWidgets.QPushButton('Back')
		button_next = QtWidgets.QPushButton('Next')

		buttons = [button_back, self.button_replay, button_next]
		button_layout = QtWidgets.QHBoxLayout()  # create a horizontal layout to hold buttons

		for button in buttons:
			self.setButtonStyle(button)
			button_layout.addWidget(button)

		# create a vertical layout to hold widgets
		otherSideEffects_layout = QtWidgets.QVBoxLayout()
		otherSideEffects_layout.addLayout(freeText_layout)
		otherSideEffects_layout.addLayout(button_layout)

		# create a widget to display the layout
		self.postSessionOtherSideEffects_widget = QtWidgets.QWidget()
		self.postSessionOtherSideEffects_widget.setLayout(otherSideEffects_layout)

		# start the audio
		# self.audioFile = self.audioPath + '.wav'
		# self.buttonsToDisable = buttons
		# if not self.isMute: self.playAudio()

		# button click connections
		button_back.clicked.connect(self.gotoPreviousWidget)
		button_next.clicked.connect(self.startPostSessionDiseasePainLayout)

	def startPostSessionDiseasePainLayout(self):
		global ongoingSpeech
		if not ongoingSpeech:
			if self.postSessionSideEffects:
				self.values['Post-Session Other Side Effects Text'] = self.plainTextEdit_postSessionOtherSideEffects.toPlainText()
			else:
				self.values['Post-Session Other Side Effects Text'] = ''
				self.values['Post-Session Headset-Related Side Effects'] = 'No'
			self.postSessionDiseasePainLayout()  # create the post-session disease pain layout
			self.stacked_layout.addWidget(self.postSessionDiseasePain_widget)  # add this to the stacked layout
			self.stacked_layout.setCurrentIndex(self.index)  # change the visible layout in the stack
			self.index += 1

	def postSessionDiseasePainLayout(self):
		label = 'Do you have or feel any disease specific pain? Please indicate how much using the visual analog scale below.'
		label_post_session_ms_pain = QtWidgets.QLabel(label)
		self.setFontStyle(label_post_session_ms_pain)

		# add MS pain visual analogue scale image to QtWidgets.QLabel
		label_MS_pain = QtWidgets.QLabel(self)
		pixmap_MS_pain = QtGui.QPixmap('data/images/visual_MS_pain.jpg')
		label_MS_pain.setPixmap(pixmap_MS_pain.scaledToWidth(self.WIDTH * 0.4, QtCore.Qt.SmoothTransformation))

		self.radioButtonList_postMSPain = []
		radioButton_layout = QtWidgets.QHBoxLayout()
		radioButton_group = QtWidgets.QButtonGroup(self)
		radioButton_group.setExclusive(True)
		for i in range(11):
			radioButton = QtWidgets.QRadioButton(str(i))
			self.setRadioButtonStyle(radioButton)
			radioButton_group.addButton(radioButton, i)
			self.radioButtonList_postMSPain.append(radioButton)
			radioButton_layout.addWidget(radioButton)
			radioButton.toggled.connect(lambda:self.recordRadioButtonSelection(self.radioButtonList_postMSPain, 'Post-Session MS pain'))
		self.setRadioButtonLayoutStyle(radioButton_layout)

		msPainScale_layout = QtWidgets.QVBoxLayout()
		msPainScale_layout.addWidget(label_MS_pain, QtCore.Qt.AlignCenter, QtCore.Qt.AlignCenter)
		msPainScale_layout.addLayout(radioButton_layout)
		self.setVisualAnalogScaleSpacing(msPainScale_layout)

		self.values['Post-Session MS pain'] = 0

		button_back = QtWidgets.QPushButton('Back')
		button_next = QtWidgets.QPushButton('Next')

		buttons = [button_back, self.button_replay, button_next]
		button_layout = QtWidgets.QHBoxLayout()  # create a horizontal layout to hold buttons

		for button in buttons:
			self.setButtonStyle(button)
			button_layout.addWidget(button)

		# create a vertical layout to hold widgets
		postSessionDiseasePain_layout = QtWidgets.QVBoxLayout()
		postSessionDiseasePain_layout.addWidget(label_post_session_ms_pain)
		postSessionDiseasePain_layout.addLayout(msPainScale_layout)
		postSessionDiseasePain_layout.addLayout(button_layout)

		# create a widget to display the layout
		self.postSessionDiseasePain_widget = QtWidgets.QWidget()
		self.postSessionDiseasePain_widget.setLayout(postSessionDiseasePain_layout)

		# start the audio
		self.audioFile = self.audioPath + 'disease_specific_pain.wav'
		self.buttonsToDisable = buttons
		if not self.isMute: self.playAudio()

		# button click connections
		button_back.clicked.connect(self.gotoPreviousWidget)
		button_next.clicked.connect(self.startPostSessionFatigueLayout)

	def startPostSessionFatigueLayout(self):
		global ongoingSpeech
		if not ongoingSpeech:
			selected = False
			for radioButton in self.radioButtonList_postMSPain:
				if radioButton.isChecked():
					selected = True
					break
			if not selected:
				QtWidgets.QMessageBox.critical(self, 'Disease specific pain',
					'Please enter the intensity of your disease specific pain before continuing further.', QtWidgets.QMessageBox.Ok)
			else:
				self.postSessionFatigueLayout()  # create the post-session fatigue layout
				self.stacked_layout.addWidget(self.postSessionFatigue_widget)  # add this to the stacked layout
				self.stacked_layout.setCurrentIndex(self.index)  # change the visible layout in the stack
				self.index += 1

	def postSessionFatigueLayout(self):
		label = 'Please rate your current level of fatigue.'
		label_post_session_fatigue = QtWidgets.QLabel(label)
		self.setFontStyle(label_post_session_fatigue)

		# add fatigue visual analogue scale image to QtWidgets.QLabel
		label_fatigue = QtWidgets.QLabel(self)
		pixmap_fatigue = QtGui.QPixmap('data/images/visual_fatigue.jpg')
		label_fatigue.setPixmap(pixmap_fatigue.scaledToWidth(self.WIDTH * 0.4, QtCore.Qt.SmoothTransformation))

		self.radioButtonList_postFatigue = []
		radioButton_layout = QtWidgets.QHBoxLayout()
		radioButton_group = QtWidgets.QButtonGroup(self)
		radioButton_group.setExclusive(True)
		for i in range(11):
			radioButton = QtWidgets.QRadioButton(str(i))
			self.setRadioButtonStyle(radioButton)
			radioButton_group.addButton(radioButton, i)
			self.radioButtonList_postFatigue.append(radioButton)
			radioButton_layout.addWidget(radioButton)
			radioButton.toggled.connect(lambda:self.recordRadioButtonSelection(self.radioButtonList_postFatigue, 'Post-Session Fatigue'))
		self.setRadioButtonLayoutStyle(radioButton_layout)

		fatigueScale_layout = QtWidgets.QVBoxLayout()
		fatigueScale_layout.addWidget(label_fatigue, QtCore.Qt.AlignCenter, QtCore.Qt.AlignCenter)
		fatigueScale_layout.addLayout(radioButton_layout)
		self.setVisualAnalogScaleSpacing(fatigueScale_layout)

		self.values['Post-Session Fatigue'] = 0

		button_back = QtWidgets.QPushButton('Back')
		button_next = QtWidgets.QPushButton('Next')

		buttons = [button_back, self.button_replay, button_next]
		button_layout = QtWidgets.QHBoxLayout()  # create a horizontal layout to hold buttons

		for button in buttons:
			self.setButtonStyle(button)
			button_layout.addWidget(button)

		# create a vertical layout to hold widgets
		postSessionFatigue_layout = QtWidgets.QVBoxLayout()
		postSessionFatigue_layout.addWidget(label_post_session_fatigue)
		postSessionFatigue_layout.addLayout(fatigueScale_layout)
		postSessionFatigue_layout.addLayout(button_layout)

		# create a widget to display the layout
		self.postSessionFatigue_widget = QtWidgets.QWidget()
		self.postSessionFatigue_widget.setLayout(postSessionFatigue_layout)

		# start the audio
		self.audioFile = self.audioPath + 'fatigue.wav'
		self.buttonsToDisable = buttons
		if not self.isMute: self.playAudio()

		# button click connections
		button_back.clicked.connect(self.gotoPreviousWidget)
		button_next.clicked.connect(self.startPostSessionPanasQuestionnaireLayout)

	def startPostSessionPanasQuestionnaireLayout(self):
		global ongoingSpeech
		if not ongoingSpeech:
			selected = False
			for radioButton in self.radioButtonList_postFatigue:
				if radioButton.isChecked():
					selected = True
					break
			if not selected:
				QtWidgets.QMessageBox.critical(self, 'Fatigue',
					'Please enter the intensity of your fatigue before continuing further.', QtWidgets.QMessageBox.Ok)
			else:
				self.postSessionPanasQuestionnaireLayout()  # create the PANAS questionnaire layout
				self.stacked_layout.addWidget(self.postSessionPanasQuestionnaire_widget)  # add this to the stacked layout
				self.stacked_layout.setCurrentIndex(self.index)  # change the visible layout in the stack
				self.index += 1

	def postSessionPanasQuestionnaireLayout(self):
		label = 'Please indicate to what extent you are feeling this way right now.'
		label_panas = QtWidgets.QLabel(label)
		self.setFontStyle(label_panas)

		N_ROWS, N_COLS = 20, 5

		self.postSessionPanasTable_widget = QtWidgets.QTableWidget()
		self.postSessionPanasTable_widget.setRowCount(N_ROWS)
		self.postSessionPanasTable_widget.setColumnCount(N_COLS)
		self.setTableStyle(self.postSessionPanasTable_widget)

		panas_col_headers = ['Very slightly or not at all', 'A little', 'Moderately', 'Quite a bit', 'Extremely']
		self.postSessionPanasTable_widget.setHorizontalHeaderLabels(panas_col_headers)

		self.postSessionPanasTable_widget.setVerticalHeaderLabels(self.panas_row_headers)

		self.panas_buttons = [[None] * N_COLS for _ in range(N_ROWS)]

		for r in range(N_ROWS):
			rating_button_group = QtWidgets.QButtonGroup(self)
			rating_button_group.setExclusive(True)
			for c in range(N_COLS):
				radio_button = QtWidgets.QRadioButton(str(c+1))
				self.postSessionPanasTable_widget.setCellWidget(r, c, radio_button)
				rating_button_group.addButton(radio_button, c)
				self.panas_buttons[r][c] = radio_button

		header = self.postSessionPanasTable_widget.horizontalHeader()
		header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)
		header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
		header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
		header.setSectionResizeMode(3, QtWidgets.QHeaderView.Stretch)
		header.setSectionResizeMode(4, QtWidgets.QHeaderView.Stretch)

		self.postSessionPanasTable_widget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)  # disable editing of content
		self.postSessionPanasTable_widget.setWordWrap(True)

		button_back = QtWidgets.QPushButton('Back')
		button_next = QtWidgets.QPushButton('Next')

		buttons = [button_back, self.button_replay, button_next]
		button_layout = QtWidgets.QHBoxLayout()  # create a horizontal layout to hold buttons

		for button in buttons:
			self.setButtonStyle(button)
			button_layout.addWidget(button)

		# create a vertical layout to hold widgets
		panasQuestionnaire_layout = QtWidgets.QVBoxLayout()
		panasQuestionnaire_layout.addWidget(label_panas)
		panasQuestionnaire_layout.addWidget(self.postSessionPanasTable_widget)
		panasQuestionnaire_layout.addLayout(button_layout)

		# create a widget to display the layout
		self.postSessionPanasQuestionnaire_widget = QtWidgets.QWidget()
		self.postSessionPanasQuestionnaire_widget.setLayout(panasQuestionnaire_layout)

		# start the audio
		self.audioFile = self.audioPath + 'panas.wav'
		self.buttonsToDisable = buttons
		if not self.isMute: self.playAudio()

		# button click connections
		button_back.clicked.connect(self.gotoPreviousWidget)
		button_next.clicked.connect(self.startTechnicalProblemsLayout)

	def startTechnicalProblemsLayout(self):
		global ongoingSpeech
		if not ongoingSpeech:
			count_selected = 0
			for r, buttons in enumerate(self.panas_buttons):
				selected = False
				for c, button in enumerate(buttons):
					if button.isChecked():
						selected = True
						count_selected += 1
						self.values['Post-Session PANAS: ' + self.panas_row_headers[r]] = c+1
				if not selected:
					self.setTableRowBackgroundColor(self.postSessionPanasTable_widget, r, '#FFFF00')
				else:
					self.setTableRowBackgroundColor(self.postSessionPanasTable_widget, r, '#FFFFFF')

			if count_selected == len(self.panas_row_headers):
				self.technicalProblemsLayout()  # create the final layout
				self.stacked_layout.addWidget(self.technicalProblems_widget)  # add this to the stacked layout
				self.stacked_layout.setCurrentIndex(self.index)  # change the visible layout in the stack
				self.index += 1
			else:
				QtWidgets.QMessageBox.critical(self, 'Incomplete answers',
					'Please select values for all parameters before continuing further.', QtWidgets.QMessageBox.Ok)

	def technicalProblemsLayout(self):
		label1 = 'FOR TECHNICIAN USE ONLY. '
		label_technicianUse = QtWidgets.QLabel(label1)
		self.setFontStyle(label_technicianUse)

		label2 = 'Were there any problems during this session?'
		label_technicalProblems = QtWidgets.QLabel(label2)
		self.setFontStyle(label_technicalProblems)

		self.plainTextEdit_comments = QtWidgets.QPlainTextEdit()
		self.plainTextEdit_comments.resize(self.WIDTH * 0.08, self.HEIGHT * 0.15)
		self.setPlainTextEditStyle(self.plainTextEdit_comments)

		comments_layout = QtWidgets.QVBoxLayout()
		comments_layout.addWidget(label_technicianUse)
		comments_layout.addWidget(label_technicalProblems)
		comments_layout.addWidget(self.plainTextEdit_comments)
		comments_layout.setContentsMargins(self.WIDTH * 0, self.HEIGHT * 0.10, self.WIDTH * 0, self.HEIGHT * 0.10)

		button_back = QtWidgets.QPushButton('Back')
		button_next = QtWidgets.QPushButton('Next')

		buttons = [button_back, self.button_replay, button_next]
		button_layout = QtWidgets.QHBoxLayout()  # create a horizontal layout to hold buttons

		for button in buttons:
			self.setButtonStyle(button)
			button_layout.addWidget(button)

		# create a vertical layout to hold widgets
		technicalProblems_layout = QtWidgets.QVBoxLayout()
		technicalProblems_layout.addLayout(comments_layout)
		technicalProblems_layout.addLayout(button_layout)

		# create a widget to display the layout
		self.technicalProblems_widget = QtWidgets.QWidget()
		self.technicalProblems_widget.setLayout(technicalProblems_layout)

		# start the audio
		self.audioFile = self.audioPath + 'problems.wav'
		self.buttonsToDisable = buttons
		if not self.isMute: self.playAudio()

		# button click connections
		button_back.clicked.connect(self.gotoPreviousWidget)
		button_next.clicked.connect(self.startFinalLayout)

	def startFinalLayout(self):
		global ongoingSpeech
		if not ongoingSpeech:
			self.values['Technical Problems'] = self.plainTextEdit_comments.toPlainText()
			self.finalLayout()  # create the final layout
			self.stacked_layout.addWidget(self.finalScreen_widget)  # add this to the stacked layout
			self.stacked_layout.setCurrentIndex(self.index)  # change the visible layout in the stack
			self.index += 1

	def finalLayout(self):
		# label = 'Your session is now complete. Would you like to check in with a technician?'
		label = 'Your session is now complete'
		label_finalScreen = QtWidgets.QLabel(label)
		self.setFontStyle(label_finalScreen)

		button_back = QtWidgets.QPushButton('Back')
		button_next = QtWidgets.QPushButton('Exit')

		buttons = [button_back, self.button_replay, button_next]
		button_layout = QtWidgets.QHBoxLayout()  # create a horizontal layout to hold buttons

		for button in buttons:
			self.setButtonStyle(button)
			button_layout.addWidget(button)

		# create a vertical layout to hold widgets
		finalScreen_layout = QtWidgets.QVBoxLayout()
		finalScreen_layout.addWidget(label_finalScreen)
		finalScreen_layout.addLayout(button_layout)

		# create a widget to display the layout
		self.finalScreen_widget = QtWidgets.QWidget()
		self.finalScreen_widget.setLayout(finalScreen_layout)

		# start the audio
		self.audioFile = self.audioPath + 'session_complete.wav'
		self.buttonsToDisable = buttons
		if not self.isMute: self.playAudio(restore=False, sessionComplete=True)

		# button click connections
		button_back.clicked.connect(self.gotoPreviousWidget)
		button_next.clicked.connect(lambda:self.exitApplication(self.studyID))

		self.saveUserData()
		self.sendUserData(self.studyID)

	# ------------------------------------------------------------------------------------------
	# 		------------------------------ HELPER FUNCTIONS ------------------------------
	# ------------------------------------------------------------------------------------------

	def playAudio(self, restore=True, sessionComplete=False):
		if not self.isMute:
			self.audio = PlayAudio(self.audioFile, restore, self.buttonsToDisable)
			if restore:
				self.audio.finished.connect(self.restoreButtons)
			if sessionComplete:
				self.audio.finished.connect(self.sessionComplete)
			self.audio.start()

	def replayAudio(self):
		global ongoingSpeech
		if not ongoingSpeech and not self.isMute:
			self.audio = PlayAudio(self.audioFile, True, self.buttonsToDisable)
			self.audio.finished.connect(self.restoreButtons)
			self.audio.start()

	def restoreButtons(self):
		for buttonToDisable in self.buttonsToDisable:
			buttonToDisable.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
			buttonToDisable.setStyleSheet('background-color: None;')

	def changeMuteStatus(self):
		if self.isMute:
			self.isMute = False
			self.toolbar.removeAction(self.muteAct)
			self.toolbar.addAction(self.unmuteAct)
		else:
			self.isMute = True
			self.toolbar.removeAction(self.unmuteAct)
			self.toolbar.addAction(self.muteAct)

	def headsetPlacementIssue(self):
		global ongoingSpeech
		if not ongoingSpeech:
			choice = QtWidgets.QMessageBox.information(self, 'Information',
				'Please assemble according to picture and continue when ready',
				QtWidgets.QMessageBox.Ok | QtWidgets.QMessageBox.Help | QtWidgets.QMessageBox.Abort,
				QtWidgets.QMessageBox.Ok)
			if choice == QtWidgets.QMessageBox.Abort:
				self.exitApplication(self.studyID)
			elif choice == QtWidgets.QMessageBox.Help:
				self.help(self.studyID)

	def selectedTechnicianEmail(self, currentIndex):
		self.studyTechnicianEmail = self.dropDown_technicianEmail.currentText()
		if type(self.recipients) is list:
			if len(self.recipients) > self.NUM_DEFAULT_EMAILS:
				self.recipients.pop()
			self.recipients.append(self.studyTechnicianEmail)
		else:
			self.recipients = [self.studyTechnicianEmail]

	def sleepQuality(self, currentIndex):
		self.values['Sleep quality'] = self.dropDown_sleepQuality.currentText()

	def contactQuality(self, currentIndex):
		self.values['Contact quality'] = self.dropDown_contactQuality.currentText()

	def showProgress(self):
		duration = str(self.values['Subject tDCS dose duration'])
		numbers = re.findall(r'\d+', duration)
		numbers = map(int, numbers)
		MINS = max(numbers)
		SECS = MINS*60
		passedTime = int(time.time())-self.startTime
		QtWidgets.QApplication.processEvents()
		half_time = False

		while passedTime <= SECS:  # wait for (MINS*60) seconds
			progress = (passedTime/SECS)*100
			self.progressBar_passedTime.setValue(progress)

			if not half_time and progress >= 50:  # half session is completed
				half_time = True
				# self.addWindowOnTopFlag()
				# window.setWindowState(window.windowState() & ~QtCore.Qt.WindowMinimized | QtCore.Qt.WindowActive)
				window.activateWindow()
				self.audioFile = self.audioPath + 'midSession_pain.wav'
				self.buttonsToDisable = []

				if not self.isMute: self.playAudio()
				choice = QtWidgets.QMessageBox.question(self, 'Headset Device Pain', 'Do you feel pain from the tDCS headset?',
					QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.Yes)

				if choice == QtWidgets.QMessageBox.Yes:
					self.audioFile = self.audioPath + 'midSession_intensity.wav'
					self.buttonsToDisable = []
					if not self.isMute: self.playAudio()
					self.removeWindowOnTopFlag()
					dialog = CustomDialog(title='Intensity Level',
										  labelText='How intense is the pain from the tDCS headset?')
					if dialog.exec_():
						ongoing_session_headset_pain = dialog.getIntensityLevel()
						if int(ongoing_session_headset_pain) >= self.PAIN_THRESHOLD:
							self.highPain(self.studyID)
						self.values['Ongoing-Session Headset Device Pain'] = ongoing_session_headset_pain
					else:
						self.values['Ongoing-Session Headset Device Pain'] = 0
					self.addWindowOnTopFlag()
				else:
					self.values['Ongoing-Session Headset Device Pain'] = 0

				self.removeWindowOnTopFlag()

			passedTime = int(time.time())-self.startTime
			QtWidgets.QApplication.processEvents()

		self.audioFile = self.audioPath + 'stimulation_complete_notification.wav'
		if not self.isMute: self.playAudio(restore=False)
		self.startStimulationEndedLayout()

	def sessionComplete(self):
		self.audioFile = self.audioPath + 'clapping.wav'
		if not self.isMute: self.playAudio()

	def closeEvent(self, QCloseEvent):
		# handles quiting of the main window triggered by clicking on the close 'X' button [top-right corner]
		QCloseEvent.ignore()
		try:
			self.exitApplication(self.studyID)
		except AttributeError:
			sys.exit()


if __name__ == '__main__':
	# create a new application
	application = QtWidgets.QApplication(sys.argv)

	# create and display the splash screen
	splash_pix = QtGui.QPixmap('data/images/splash.jpg')
	splash = QtWidgets.QSplashScreen(splash_pix, QtCore.Qt.WindowStaysOnTopHint)
	splash.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint)
	splash.setEnabled(False)
	splash.setWindowIcon(QtGui.QIcon('data/images/logo.ico'))
	splash.setWindowTitle('tDCS')
	splash.show()
	application.processEvents()

	"""
	import everything here ...
	"""
	import os
	import re
	import psutil
	import pandas as pd
	from datetime import datetime

	# play audio files
	import simpleaudio as sa

	# # webcam stream
	# import cv2

	# # nose detection
	# from imutils import face_utils
	# import imutils
	# import dlib

	# # headset placement verification
	# sys.path.append("data/")
	# import numpy as np
	# import tensorflow as tf
	# from PIL import Image, ImageColor, ImageDraw, ImageFont
	# from collections import defaultdict
	# from object_detection.utils import ops as utils_ops
	# from object_detection.utils import label_map_util
	# from object_detection.utils import visualization_utils as vis_util

	# sending email
	import smtplib
	from email.mime.multipart import MIMEMultipart
	from email.mime.text import MIMEText
	from email.mime.base import MIMEBase
	from email import encoders

	"""
	start the application
	"""
	window = MainWindow()  # create a new instance of the main window
	splash.finish(window)
	window.show()  # make the instance visible
	sys.exit(application.exec_())  # monitor application for events

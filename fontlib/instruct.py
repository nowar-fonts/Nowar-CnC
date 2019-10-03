def SetHintFlag(font):
	head_ = font['head']
	head_['flags'].update({
		"baselineAtY_0": True,
		"lsbAtX_0": True,
		"alwaysUseIntegerSize": True,
		"instrMayDependOnPointSize": True,
	})

local LSM3 = LibStub("LibSharedMedia-3.0", true)
local LSM2 = LibStub("LibSharedMedia-2.0", true)
local SML = LibStub("SharedMedia-1.0", true)

NowarCnCTypeface = {}
NowarCnCTypeface.revision = tonumber(string.sub("$Revision$", 12, -3)) or 1

NowarCnCTypeface.registry = { ["font"] = {} }
NowarCnCTypeface.language = {}
NowarCnCTypeface.LSM3 = LSM3

if LSM3 then
	NowarCnCTypeface.language.koKR = LSM3.LOCALE_BIT_koKR
	NowarCnCTypeface.language.ruRU = LSM3.LOCALE_BIT_ruRU
	NowarCnCTypeface.language.zhCN = LSM3.LOCALE_BIT_zhCN
	NowarCnCTypeface.language.zhTW = LSM3.LOCALE_BIT_zhTW
	NowarCnCTypeface.language.western = LSM3.LOCALE_BIT_western
else
	NowarCnCTypeface.language.koKR = 0
	NowarCnCTypeface.language.ruRU = 0
	NowarCnCTypeface.language.zhCN = 0
	NowarCnCTypeface.language.zhTW = 0
	NowarCnCTypeface.language.western = 0
end

function NowarCnCTypeface:Register(mediatype, key, data, langmask)
	if LSM3 then
		LSM3:Register(mediatype, key, data, langmask)
	end
	if LSM2 then
		LSM2:Register(mediatype, key, data)
	end
	if SML then
		SML:Register(mediatype, key, data)
	end
	if not NowarCnCTypeface.registry[mediatype] then
		NowarCnCTypeface.registry[mediatype] = {}
	end
	table.insert(NowarCnCTypeface.registry[mediatype], { key, data, langmask})
end

function NowarCnCTypeface.OnEvent(this, event, ...)
	if not LSM3 then
		LSM3 = LibStub("LibSharedMedia-3.0", true)
		if LSM3 then
			for m,t in pairs(NowarCnCTypeface.registry) do
				for _,v in ipairs(t) do
					LSM3:Register(m, v[1], v[2], v[3])
				end
			end
		end
	end
	if not LSM2 then
		LSM2 = LibStub("LibSharedMedia-2.0", true)
		if LSM2 then
			for m,t in pairs(NowarCnCTypeface.registry) do
				for _,v in ipairs(t) do
					LSM2:Register(m, v[1], v[2])
				end
			end
		end
	end
	if not SML then
		SML = LibStub("SharedMedia-1.0", true)
		if SML then
			for m,t in pairs(NowarCnCTypeface.registry) do
				for _,v in ipairs(t) do
					SML:Register(m, v[1], v[2])
				end
			end
		end
	end
end

NowarCnCTypeface.frame = CreateFrame("Frame")
NowarCnCTypeface.frame:SetScript("OnEvent", NowarCnCTypeface.OnEvent)
NowarCnCTypeface.frame:RegisterEvent("ADDON_LOADED")

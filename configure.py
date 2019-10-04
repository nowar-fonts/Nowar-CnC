import json
import codecs
from functools import reduce
from itertools import product
from types import SimpleNamespace as Namespace

from pprint import pprint

class Config:
	version = "0.1.0"
	fontRevision = 0.0100
	vendor = "Nowar Typeface"
	vendorId = "NOWR"
	vendorUrl = "https://github.com/nowar-fonts"
	copyright = "Copyright © 2019—2020 Cyano Hao and Nowar Typeface, with reserved font name “Nowar”, “有爱”, and “有愛”. Portions Copyright 2015 Google Inc. Portions © 2014-2019 Adobe (http://www.adobe.com/)."
	designer = "Cyano Hao (character set definition, autohinting & modification for World of Warcraft); Monotype Design Team (Latin, Greek & Cyrillic); Ryoko NISHIZUKA 西塚涼子 (kana, bopomofo & ideographs); Sandoll Communications 산돌커뮤니케이션, Soo-young JANG 장수영 & Joo-yeon KANG 강주연 (hangul elements, letters & syllables); Dr. Ken Lunde (project architect, glyph set definition & overall production); Masataka HATTORI 服部正貴 (production & ideograph elements)"
	designerUrl = "https://github.com/CyanoHao"
	license = "This Font Software is licensed under the SIL Open Font License, Version 1.1. This Font Software is distributed on an \"AS IS\" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the SIL Open Font License for the specific language, permissions and limitations governing your use of this Font Software."
	licenseUrl = "https://scripts.sil.org/OFL"

	fontPackWeight = [ 200, 300, 400, 500, 700 ]
	fontPackRegion = [ "CN", "TW", "HK", "JP", "KR", "CL", "OSF", "GB", "RP" ]

	fontProviderWeight = [ 200, 300, 400, 500, 700 ]
	fontProviderWidth = [ 3, 5, 7 ]
	fontProviderInstance = {
		# seperate western to 2 parts, avoid sed argument strips
		"western1": [ Namespace(
			weight = w,
			width = wd,
			family = "UI",
			region = r,
			encoding = "unspec"
		) for w, wd, r in product(fontProviderWeight, fontProviderWidth, [ "CN", "TW", "HK", "JP" ]) ],
		"western2": [ Namespace(
			weight = w,
			width = wd,
			family = "UI",
			region = r,
			encoding = "unspec"
		) for w, wd, r in product(fontProviderWeight, fontProviderWidth, [ "CL", "OSF" ]) ],
		"zhCN": [ Namespace(
			weight = w,
			width = wd,
			family = "Sans",
			region = r,
			encoding = "unspec"
		) for w, wd, r in product(fontProviderWeight, fontProviderWidth, [ "CN", "CL" ]) ],
		"zhTW": [ Namespace(
			weight = w,
			width = wd,
			family = "Sans",
			region = r,
			encoding = "unspec"
		) for w, wd, r in product(fontProviderWeight, fontProviderWidth, [ "TW", "HK", "CL" ]) ],
		"koKR": [ Namespace(
			weight = w,
			width = wd,
			family = "Sans",
			region = r,
			encoding = "unspec"
		) for w, wd, r in product(fontProviderWeight, fontProviderWidth, [ "KR" ]) ],
	}

config = Config()

weightMap = {
	100: "Thin",
	200: "ExtraLight",
	300: "Light",
	400: "Regular",
	500: "Medium",
	600: "SemiBold",
	700: "Bold",
	800: "ExtraBold",
	900: "Black",
}

widthMap = {
	3: "Condensed",
	4: "SemiCondensed",
	5: None,
	7: "Extended",
}

notoWidthMap = {
	3: 3,
	5: 4,
	7: 5,
}

morpheusWeightMap = {
	200: 100,
	300: 200,
	400: 500,
	500: 600,
	700: 800,
}

# define font pack orthographies for diffrent WoW language
# Latn -- Chinese characters in European languages, must be defined.
# Hans -- 简体中文; if set to `None`, the font pack will not override 简体中文 font.
# Hans -- 繁體中文, can be `None`.
# ko -- 漢字 in 한국어, can be `None`.
regionalVariant = {
	"CN": {
		"Latn": "CN",
		"Hans": "CN",
		"Hant": "TW",
		"ko": "KR",
	},
	"TW": {
		"Latn": "TW",
		"Hans": "CN",
		"Hant": "TW",
		"ko": "KR",
	},
	"HK": {
		"Latn": "HK",
		"Hans": "CN",
		"Hant": "HK",
		"ko": "KR",
	},
	"JP": {
		"Latn": "JP",
		"Hans": "CN",
		"Hant": "TW",
		"ko": "KR",
	},
	"KR": {
		"Latn": "KR",
		"Hans": "CN",
		"Hant": "TW",
		"ko": "KR",
	},
	"CL": {
		"Latn": "CL",
		"Hans": "CL",
		"Hant": "CL",
		"ko": "CL",
	},
	"OSF": {
		"Latn": "OSF",
		"Hans": "CL",
		"Hant": "CL",
		"ko": "CL",
	},
	"GB": {
		"Latn": "GB",
		"Hans": "GB",
		"Hant": "GB",
		"ko": None,
	},
	"RP": {
		"Latn": "RP",
		"Hans": "RP",
		"Hant": "RP",
		"ko": None,
	},
}

# map orthography to source file
regionSourceMap = {
	"CN": "SourceHanSansSC",
	"TW": "SourceHanSansTC",
	"HK": "SourceHanSansHC",
	"JP": "SourceHanSans",
	"KR": "SourceHanSansK",
	"CL": "SourceHanSansK",
	"OSF": "SourceHanSansK",
	"GB": "SourceHanSansCN",
	"RP": "SourceHanSansCN",
}

regionNameMap = {
	"CN": "CN",
	"TW": "TW",
	"HK": "HK",
	"JP": "JP",
	"KR": "KR",
	"CL": "Classical",
	"OSF": "Oldstyle",
	"GB": "GB18030",
	"RP": "Roleplaying",
}

# set OS/2 encoding to make Windows show font icon in proper language
encoding = [
	"unspec", # 文字美
	"gbk",    # 简体字
	"big5",   # 繁體字
	"jis",    # あア亜
	"korean", # 한글
]

def GetRegion(p):
	if hasattr(p, "region"):
		return p.region
	else:
		return ""

def GenerateFamily(p):
	impl = {
		"Sans": lambda region: {
			0x0409: "Nowar C² " + regionNameMap[region],
			0x0804: "有爱锐方 " + regionNameMap[region],
			0x0404: "有愛銳方 " + regionNameMap[region],
			0x0C04: "有愛鋭方 " + regionNameMap[region],
			0x0411: "有愛鋭方 " + regionNameMap[region],
			0x0412: "有愛예방 " + regionNameMap[region],
		},
		"UI": lambda region: {
			0x0409: "Nowar C² UI " + regionNameMap[region],
			0x0804: "有爱锐方 UI " + regionNameMap[region],
			0x0404: "有愛銳方 UI " + regionNameMap[region],
			0x0C04: "有愛鋭方 UI " + regionNameMap[region],
			0x0411: "有愛鋭方 UI " + regionNameMap[region],
			0x0412: "有愛예방 UI " + regionNameMap[region],
		},
		"WarcraftSans": lambda region: {
			0x0409: "Nowar C² Warcraft " + regionNameMap[region],
			0x0804: "有爱魔兽锐方 " + regionNameMap[region],
			0x0404: "有愛魔獸銳方 " + regionNameMap[region],
			0x0C04: "有愛魔獸鋭方 " + regionNameMap[region],
			0x0411: "有愛鋭方ウォークラフト " + regionNameMap[region],
			0x0412: "有愛예방 워크래프트 " + regionNameMap[region],
		},
		"WarcraftUI": lambda region: {
			0x0409: "Nowar C² Warcraft UI " + regionNameMap[region],
			0x0804: "有爱魔兽锐方 UI " + regionNameMap[region],
			0x0404: "有愛魔獸銳方 UI " + regionNameMap[region],
			0x0C04: "有愛魔獸黑體 UI " + regionNameMap[region],
			0x0411: "有愛鋭方ウォークラフト UI " + regionNameMap[region],
			0x0412: "有愛예방 워크래프트 UI " + regionNameMap[region],
		},
		"Latin": lambda region: {
			0x0409: "Nowar C² UI LCG",
			0x0804: "Nowar C² UI LCG",
			0x0404: "Nowar C² UI LCG",
			0x0C04: "Nowar C² UI LCG",
			0x0411: "Nowar C² UI LCG",
			0x0412: "Nowar C² UI LCG",
		}
	}
	return impl[p.family](GetRegion(p))

def GenerateSubfamily(p):
	width = widthMap[p.width]
	weight = weightMap[p.weight]
	if hasattr(p, "italic") and p.italic:
		if p.weight == 400:
			return width + " Italic" if width else "Italic"
		else:
			return ("{} {}".format(width, weight) if width else weight) + " Italic"
	else:
		if p.weight == 400:
			return width if width else "Regular"
		else:
			return "{} {}".format(width, weight) if width else weight

def GenerateFriendlyFamily(p):
	return { k: "{} {}".format(v, GenerateSubfamily(p)) for k, v in GenerateFamily(p).items() }

def GenerateLegacySubfamily(p):
	width = widthMap[p.width]
	weight = weightMap[p.weight]
	if hasattr(p, "italic") and p.italic:
		if p.weight == 400:
			return width or "", "Italic"
		elif p.weight == 700:
			return width or "", "Bold Italic"
		else:
			return "{} {}".format(width, weight) if width else weight, "Italic"
	else:
		if p.weight == 400 or p.weight == 700:
			return width or "", weight
		else:
			return "{} {}".format(width, weight) if width else weight, "Regular"

def GenerateFilename(p):
	familyName = {
		"Sans": lambda region: "NowarCnC-" + region,
		"UI": lambda region: "NowarCnCUI-" + region,
		"WarcraftSans": lambda region: "NowarCnCWarcraft-" + region,
		"WarcraftUI": lambda region: "NowarCnCWarcraftUI-" + region,
		"Latin": lambda region: "NowarCnC",
		"Noto": lambda region: "NotoSans",
		"Source": lambda region: region,
	}
	return (p.encoding + "-" if p.family in [ "Sans", "UI", "WarcraftSans", "WarcraftUI" ] else "") + familyName[p.family](GetRegion(p)) + "-" + GenerateSubfamily(p).replace(" ", "")

def ResolveDependency(p):
	result = {
		"Latin": Namespace(
			family = "Noto",
			width = notoWidthMap[p.width],
			weight = p.weight
		)
	}
	if p.family in [ "WarcraftSans", "WarcraftUI" ]:
		result["Numeral"] = Namespace(
			family = "Noto",
			width = 3,
			weight = p.weight
		)
	if p.family in [ "Sans", "UI", "WarcraftSans", "WarcraftUI" ]:
		result["CJK"] = Namespace(
			family = "Source",
			weight = p.weight,
			width = 5,
			region = regionSourceMap[p.region]
		)
	return result

def GetMorpheus(weight):
	return Namespace(
		weight = morpheusWeightMap[weight],
		width = 3,
		family = "Latin"
	)

def GetSkurri(weight):
	return Namespace(
		weight = weight,
		width = 7,
		family = "Latin"
	)

def GetLatinFont(weight, region):
	return Namespace(
		weight = weight,
		width = 7,
		family = "UI",
		region = regionalVariant[region]["Latn"],
		encoding = "unspec"
	)

def GetLatinChatFont(weight, region):
	return Namespace(
		weight = weight,
		width = 3,
		family = "UI",
		region = regionalVariant[region]["Latn"],
		encoding = "unspec"
	)

def GetHansFont(weight, region):
	return Namespace(
		weight = weight,
		width = 5,
		family = "WarcraftSans",
		region = regionalVariant[region]["Hans"],
		encoding = "gbk"
	)

def GetHansCombatFont(weight, region):
	return Namespace(
		weight = weight,
		width = 7,
		family = "Sans",
		region = regionalVariant[region]["Hans"],
		encoding = "gbk"
	)

def GetHansChatFont(weight, region):
	return Namespace(
		weight = weight,
		width = 3,
		family = "Sans",
		region = regionalVariant[region]["Hans"],
		encoding = "gbk"
	)

def GetHantFont(weight, region):
	return Namespace(
		weight = weight,
		width = 5,
		family = "WarcraftSans",
		region = regionalVariant[region]["Hant"],
		encoding = "big5"
	)

def GetHantCombatFont(weight, region):
	return Namespace(
		weight = weight,
		width = 7,
		family = "Sans",
		region = regionalVariant[region]["Hant"],
		encoding = "big5"
	)

def GetHantNoteFont(weight, region):
	return Namespace(
		weight = weight,
		width = 5,
		family = "Sans",
		region = regionalVariant[region]["Hant"],
		encoding = "big5"
	)

def GetHantChatFont(weight, region):
	return Namespace(
		weight = weight,
		width = 3,
		family = "Sans",
		region = regionalVariant[region]["Hant"],
		encoding = "big5"
	)


def GetKoreanFont(weight, region):
	return Namespace(
		weight = weight,
		width = 5,
		family = "Sans",
		region = regionalVariant[region]["ko"],
		encoding = "korean"
	)

def GetKoreanCombatFont(weight, region):
	return Namespace(
		weight = weight,
		width = 7,
		family = "Sans",
		region = regionalVariant[region]["ko"],
		encoding = "korean"
	)

def GetKoreanDisplayFont(weight, region):
	return Namespace(
		weight = weight,
		width = 3,
		family = "Sans",
		region = regionalVariant[region]["ko"],
		encoding = "korean"
	)

def ParamToArgument(conf):
	escapeList = [ ' ', '"', '{', '}' ]
	js = json.dumps(conf.__dict__)
	for c in escapeList:
		js = js.replace(c, '\\' + c)
	return js

if __name__ == "__main__":
	makefile = {
		"variable": {
			"VERSION": config.version,
			"IDH_JOBS?": 1,
		},
		"rule": {
			".PHONY": {
				"depend": [
					"all",
					"hint2",
				] + [
					"hint2-{}".format(w) for w in config.fontPackWeight
				],
			},
			"all": {
				"depend": [ "out/SharedMedia-NowarSans-${VERSION}.7z" ],
			},
			"clean": {
				"command": [
					"-rm -rf build/",
					"-rm -rf out/NowarCnCTypeface",
					"-rm -rf " + " ".join([ "out/{}-{}/".format(r, w) for r, w in product(config.fontPackRegion, config.fontPackWeight) ]),
				],
			},
		},
	}

	hintInstance = []
	unique = lambda l: reduce(lambda l, x: l + [ x ] if x not in l else l, l, [])

	# SharedMedia font provider
	hintInstance += sum(config.fontProviderInstance.values(), [])
	makefile["rule"]["out/SharedMedia-NowarSans-${VERSION}.7z"] = {
		"depend": [ "build/nowar/{}.ttf".format(GenerateFilename(p)) for p in sum(config.fontProviderInstance.values(), []) ],
		"command": [
			# copy interface directory
			"mkdir -p out/",
			"cp -r source/libsm out/NowarCnCTypeface",
			"cp LICENSE.txt out/NowarCnCTypeface/",
			"mkdir -p out/NowarCnCTypeface/Fonts/",
			# replace dummy strings
			"sed -i 's/__REPLACE_IN_BUILD__VERSION__/${VERSION}/' out/NowarCnCTypeface/NowarCnCTypeface.toc",
			"sed -i '/__REPLACE_IN_BUILD__REGISTER_WESTERN1__/{{s/__REPLACE_IN_BUILD__REGISTER_WESTERN1__/{}/}}' out/NowarCnCTypeface/NowarCnCTypeface.lua".format(
				"\\n".join(
					[
						# backslashes will be escaped twice by `make` and `sed`
						r'NowarCnCTypeface:Register("font", "{}", [[Interface\\\\Addons\\\\NowarCnCTypeface\\\\Fonts\\\\{}.ttf]], western + ruRU)'.format(
							GenerateFriendlyFamily(p)[0x0409],
							GenerateFilename(p).replace("unspec-", "")
						) for p in config.fontProviderInstance["western1"]
					]
				)
			),
			"sed -i '/__REPLACE_IN_BUILD__REGISTER_WESTERN2__/{{s/__REPLACE_IN_BUILD__REGISTER_WESTERN2__/{}/}}' out/NowarCnCTypeface/NowarCnCTypeface.lua".format(
				"\\n".join(
					[
						r'NowarCnCTypeface:Register("font", "{}", [[Interface\\\\Addons\\\\NowarCnCTypeface\\\\Fonts\\\\{}.ttf]], western + ruRU)'.format(
							GenerateFriendlyFamily(p)[0x0409],
							GenerateFilename(p).replace("unspec-", "")
						) for p in config.fontProviderInstance["western2"]
					]
				)
			),
			"sed -i '/__REPLACE_IN_BUILD__REGISTER_ZHCN__/{{s/__REPLACE_IN_BUILD__REGISTER_ZHCN__/{}/}}' out/NowarCnCTypeface/NowarCnCTypeface.lua".format(
				"\\n".join(
					[
						r'NowarCnCTypeface:Register("font", "{}", [[Interface\\\\Addons\\\\NowarCnCTypeface\\\\Fonts\\\\{}.ttf]], zhCN)'.format(
							GenerateFriendlyFamily(p)[0x0804],
							GenerateFilename(p).replace("unspec-", "")
						) for p in config.fontProviderInstance["zhCN"]
					]
				)
			),
			"sed -i '/__REPLACE_IN_BUILD__REGISTER_ZHTW__/{{s/__REPLACE_IN_BUILD__REGISTER_ZHTW__/{}/}}' out/NowarCnCTypeface/NowarCnCTypeface.lua".format(
				"\\n".join(
					[
						r'NowarCnCTypeface:Register("font", "{}", [[Interface\\\\Addons\\\\NowarCnCTypeface\\\\Fonts\\\\{}.ttf]], zhTW)'.format(
							GenerateFriendlyFamily(p)[0x0404],
							GenerateFilename(p).replace("unspec-", "")
						) for p in config.fontProviderInstance["zhTW"]
					]
				)
			),
			"sed -i '/__REPLACE_IN_BUILD__REGISTER_KOKR__/{{s/__REPLACE_IN_BUILD__REGISTER_KOKR__/{}/}}' out/NowarCnCTypeface/NowarCnCTypeface.lua".format(
				"\\n".join(
					[
						r'NowarCnCTypeface:Register("font", "{}", [[Interface\\\\Addons\\\\NowarCnCTypeface\\\\Fonts\\\\{}.ttf]], koKR)'.format(
							GenerateFriendlyFamily(p)[0x0412],
							GenerateFilename(p).replace("unspec-", "")
						) for p in config.fontProviderInstance["koKR"]
					]
				)
			),
			# copy font files
			"for file in $^; do cp $$file out/NowarCnCTypeface/Fonts/$${file#out/nowar/*-}; done",
			# pack with 7z, group them by weight to generate smaller file in less time
			"cd out/; 7z a -t7z -m0=LZMA:d=512m:fb=273 -ms ../$@ NowarCnCTypeface/ -x!NowarCnCTypeface/Fonts/\\*.ttf",
		] + [
			"cd out/; 7z a -t7z -m0=LZMA:d=512m:fb=273 -ms ../$@ " + " ".join([
				"NowarCnCTypeface/Fonts/{}.ttf".format(GenerateFilename(p).replace("unspec-", ""))
					for p in unique(sum(config.fontProviderInstance.values(), []))
					if p.weight == w
			]) for w in config.fontProviderWeight
		]
	}

	# font pack for each regional variant and weight
	for r, w in product(config.fontPackRegion, config.fontPackWeight):
		target = "{}-{}".format(r, w)
		pack = "out/NowarSans-{}-${{VERSION}}.7z".format(target)
		makefile["rule"]["all"]["depend"].append(pack)
		fontlist = {
			"ARIALN": GetLatinChatFont(w, r),
			"FRIZQT__": GetLatinFont(w, r),
			"MORPHEUS": GetMorpheus(w),
			"skurri": GetSkurri(w),

			"FRIZQT___CYR": GetLatinFont(w, r),
			"MORPHEUS_CYR": GetMorpheus(w),
			"SKURRI_CYR": GetSkurri(w),
		}

		if regionalVariant[r]["Hans"]:
			fontlist.update({
				"ARKai_C": GetHansCombatFont(w, r),
				"ARKai_T": GetHansFont(w, r),
				"ARHei": GetHansChatFont(w, r),
			})

		if regionalVariant[r]["Hant"]:
			fontlist.update({
				"arheiuhk_bd": GetHantChatFont(w, r),
				"bHEI00M": GetHantNoteFont(w, r),
				"bHEI01B": GetHantChatFont(w, r),
				"bKAI00M": GetHantCombatFont(w, r),
				"blei00d": GetHantFont(w, r),
			})

		if regionalVariant[r]["ko"]:
			fontlist.update({
				"2002": GetKoreanFont(w, r),
				"2002B": GetKoreanFont(w, r),
				"K_Damage": GetKoreanCombatFont(w, r),
				"K_Pagetext": GetKoreanDisplayFont(w, r),
			})

		hintInstance += list(fontlist.values())
		makefile["rule"][pack] = {
			"depend": [ "out/{}/Fonts/{}.ttf".format(target, f) for f in fontlist ],
			"command": [
				"cd out/{};".format(target) +
				"cp ../../LICENSE.txt Fonts/LICENSE.txt;" +
				"7z a -t7z -m0=LZMA:d=512m:fb=273 -ms ../../$@ Fonts/"
			]
		}

		for f, p in fontlist.items():
			makefile["rule"]["out/{}/Fonts/{}.ttf".format(target, f)] = {
				"depend": [ "build/nowar/{}.ttf".format(GenerateFilename(p)) ],
				"command": [
					"mkdir -p out/{}/Fonts".format(target),
					"cp $^ $@",
				]
			}

	hintGroup = {
		"Latin": []
	}
	hintGroup.update({
		w: [] for w in config.fontPackWeight
	})
	for f in hintInstance:
		if f.family == "Latin":
			hintGroup["Latin"].append(f)
		else:
			f.encoding = "unspec"
			hintGroup[f.weight].append(f)
	for k, v in hintGroup.items():
		hintGroup[k] = unique(v)
	# pprint(hintGroup)

	# IDH
	makefile["rule"]["hint2"] = {
		"depend": [ "hint2-{}".format(w) for w in config.fontPackWeight ],
	}
	for w in config.fontPackWeight:
		makefile["rule"]["hint2-{}".format(w)] = {
			"depend": [ "build/hint2/{}.otd".format(GenerateFilename(f)) for f in hintGroup[w] ],
			"command": [
				"node --max-old-space-size=8192 node_modules/@chlorophytum/cli/lib/index.js hint -c source/idh/{0}.json -h cache/idh-{0}.gz -j ${{IDH_JOBS}} ".format(w) +
				" ".join([ "build/hint2/{0}.otd build/hint2/{0}.hint.gz".format(GenerateFilename(f)) for f in hintGroup[w] ])
			],
		}
		for f in hintGroup[w]:
			makefile["rule"]["build/nowar/{}.ttf".format(GenerateFilename(f))] = {
				"depend": [ "build/nowar/{}.otd".format(GenerateFilename(f)) ],
				"command": [ "otfccbuild -O3 --keep-average-char-width $< -o $@ 2>/dev/null" ],
			}
			makefile["rule"]["build/nowar/{}.otd".format(GenerateFilename(f))] = {
				"depend": [ "build/hint2/{}.instr.gz".format(GenerateFilename(f)) ],
				"command": [
					"mkdir -p build/nowar/",
					"node --max-old-space-size=8192 node_modules/@chlorophytum/cli/lib/index.js integrate -c source/idh/{0}.json build/hint2/{1}.instr.gz build/hint2/{1}.otd build/nowar/{1}.otd".format(w, GenerateFilename(f)),
				],
			}
			makefile["rule"]["build/hint2/{}.instr.gz".format(GenerateFilename(f))] = {
				"depend": [ "build/hint2/{}.hint.gz".format(GenerateFilename(f)) ],
				"command": [
					"node --max-old-space-size=8192 node_modules/@chlorophytum/cli/lib/index.js instruct -c source/idh/{0}.json build/hint2/{1}.otd build/hint2/{1}.hint.gz build/hint2/{1}.instr.gz".format(w, GenerateFilename(f)),
				],
			}
			makefile["rule"]["build/hint2/{}.hint.gz".format(GenerateFilename(f))] = {
				"depend": [ "hint2" ],
			}
			makefile["rule"]["build/hint2/{}.otd".format(GenerateFilename(f))] = {
				"depend": [ "build/hint1/{}.ttf".format(GenerateFilename(f)) ],
				"command": [
					"mkdir -p build/hint2/",
					"otfccdump $< -o $@",
				],
			}

	# TTFautohint
	for f in hintGroup["Latin"]:
		makefile["rule"]["build/nowar/{}.ttf".format(GenerateFilename(f))] = {
			"depend": [ "build/unhinted/{}.ttf".format(GenerateFilename(f)) ],
			"command": [
				"mkdir -p build/nowar/",
				"ttfautohint -a qqq -c -D latn -f latn -G 0 -l 7 -r 48 -n -x 0 -v $< $@",
			],
		}
	for w in config.fontPackWeight:
		for f in hintGroup[w]:
			makefile["rule"]["build/hint1/{}.ttf".format(GenerateFilename(f))] = {
				"depend": [ "build/unhinted/{}.ttf".format(GenerateFilename(f)) ],
				"command": [
					"mkdir -p build/hint1/",
					"ttfautohint -a qqq -c -D latn -f latn -G 0 -l 7 -r 48 -n -x 0 -v $< $@",
				],
			}

	# Sans, UI
	for f, w, wd, r in product([ "Sans", "UI" ], config.fontPackWeight, [3, 5, 7], regionNameMap.keys()):
		param = Namespace(
			family = f,
			weight = w,
			width = wd,
			region = r,
			encoding = "unspec",
		)
		makefile["rule"]["build/unhinted/{}.ttf".format(GenerateFilename(param))] = {
			"depend": ["build/unhinted/{}.otd".format(GenerateFilename(param))],
			"command": [ "otfccbuild -O3 --keep-average-char-width $< -o $@ 2>/dev/null" ]
		}
		dep = ResolveDependency(param)
		makefile["rule"]["build/unhinted/{}.otd".format(GenerateFilename(param))] = {
			"depend": [
				"build/noto/{}.otd".format(GenerateFilename(dep["Latin"])),
				"build/shs/{}.otd".format(GenerateFilename(dep["CJK"])),
			],
			"command": [ 
				"mkdir -p build/unhinted/",
				"python merge.py {}".format(ParamToArgument(param)),
			]
		}
		makefile["rule"]["build/noto/{}.otd".format(GenerateFilename(dep["Latin"]))] = {
			"depend": [ "source/noto/{}.ttf".format(GenerateFilename(dep["Latin"])) ],
			"command": [
				"mkdir -p build/noto/",
				"otfccdump --ignore-hints $< -o $@",
			]
		}
		makefile["rule"]["build/shs/{}.otd".format(GenerateFilename(dep["CJK"]))] = {
			"depend": [ "build/shs/{}.ttf".format(GenerateFilename(dep["CJK"])) ],
			"command": [ "otfccdump --ignore-hints $< -o $@" ]
		}
		makefile["rule"]["build/shs/{}.ttf".format(GenerateFilename(dep["CJK"]))] = {
			"depend": [ "source/shs/{}.otf".format(GenerateFilename(dep["CJK"])) ],
			"command": [
				"mkdir -p build/shs/",
				"otfccdump --ignore-hints $< | node node_modules/otfcc-c2q/_c2q_startup.js | otfccbuild -O3 -o $@",
			],
		}

		# set encoding
		for e in [ "gbk", "big5", "jis", "korean" ]:
			enc = Namespace(
				family = f,
				weight = w,
				width = wd,
				region = r,
				encoding = e,
			)
			makefile["rule"]["build/nowar/{}.ttf".format(GenerateFilename(enc))] = {
				"depend": ["build/nowar/{}.otd".format(GenerateFilename(enc))],
				"command": [ "otfccbuild -O3 --keep-average-char-width $< -o $@ 2>/dev/null" ]
			}
			makefile["rule"]["build/nowar/{}.otd".format(GenerateFilename(enc))] = {
				"depend": ["build/nowar/{}.otd".format(GenerateFilename(param))],
				"command": [ "python set-encoding.py {}".format(ParamToArgument(enc)) ]
			}

	# WarcraftSans
	for w, r in product(config.fontPackWeight, regionNameMap.keys()):
		param = Namespace(
			family = "WarcraftSans",
			weight = w,
			width = 5,
			region = r,
			encoding = "unspec",
		)
		makefile["rule"]["build/unhinted/{}.ttf".format(GenerateFilename(param))] = {
			"depend": ["build/unhinted/{}.otd".format(GenerateFilename(param))],
			"command": [ "otfccbuild -O3 --keep-average-char-width $< -o $@ 2>/dev/null" ]
		}
		dep = ResolveDependency(param)
		makefile["rule"]["build/unhinted/{}.otd".format(GenerateFilename(param))] = {
			"depend": [
				"build/noto/{}.otd".format(GenerateFilename(dep["Latin"])),
				"build/noto/{}.otd".format(GenerateFilename(dep["Numeral"])),
				"build/shs/{}.otd".format(GenerateFilename(dep["CJK"])),
			],
			"command": [ 
				"mkdir -p build/unhinted/",
				"python merge.py {}".format(ParamToArgument(param))
			]
		}
		makefile["rule"]["build/noto/{}.otd".format(GenerateFilename(dep["Latin"]))] = {
			"depend": [ "source/noto/{}.ttf".format(GenerateFilename(dep["Latin"])) ],
			"command": [
				"mkdir -p build/noto/",
				"otfccdump --ignore-hints $< -o $@",
			]
		}
		makefile["rule"]["build/noto/{}.otd".format(GenerateFilename(dep["Numeral"]))] = {
			"depend": [ "source/noto/{}.ttf".format(GenerateFilename(dep["Numeral"])) ],
			"command": [
				"mkdir -p build/noto/",
				"otfccdump --ignore-hints $< -o $@",
			]
		}
		makefile["rule"]["build/shs/{}.otd".format(GenerateFilename(dep["CJK"]))] = {
			"depend": [ "build/shs/{}.ttf".format(GenerateFilename(dep["CJK"])) ],
			"command": [ "otfccdump --ignore-hints $< -o $@" ]
		}
		makefile["rule"]["build/shs/{}.ttf".format(GenerateFilename(dep["CJK"]))] = {
			"depend": [ "source/shs/{}.otf".format(GenerateFilename(dep["CJK"])) ],
			"command": [
				"mkdir -p build/shs/",
				"otfccdump --ignore-hints $< | node node_modules/otfcc-c2q/_c2q_startup.js | otfccbuild -O3 -o $@",
			],
		}

		for e in [ "gbk", "big5", "jis", "korean" ]:
			enc = Namespace(
				family = "WarcraftSans",
				weight = w,
				width = 5,
				region = r,
				encoding = e,
			)
			makefile["rule"]["build/nowar/{}.ttf".format(GenerateFilename(enc))] = {
				"depend": ["build/nowar/{}.otd".format(GenerateFilename(enc))],
				"command": [ "otfccbuild -O3 --keep-average-char-width $< -o $@ 2>/dev/null" ]
			}
			makefile["rule"]["build/nowar/{}.otd".format(GenerateFilename(enc))] = {
				"depend": ["build/nowar/{}.otd".format(GenerateFilename(param))],
				"command": [ "python set-encoding.py {}".format(ParamToArgument(enc)) ]
			}

	# Latin
	for w, wd in product(config.fontPackWeight + [ morpheusWeightMap[w] for w in config.fontPackWeight ], [3, 5, 7]):
		param = Namespace(
			family = "Latin",
			weight = w,
			width = wd,
		)
		makefile["rule"]["build/unhinted/{}.ttf".format(GenerateFilename(param))] = {
			"depend": ["build/unhinted/{}.otd".format(GenerateFilename(param))],
			"command": [ "otfccbuild -O3 --keep-average-char-width $< -o $@ 2>/dev/null" ]
		}
		dep = ResolveDependency(param)
		makefile["rule"]["build/unhinted/{}.otd".format(GenerateFilename(param))] = {
			"depend": [
				"build/noto/{}.otd".format(GenerateFilename(dep["Latin"])),
			],
			"command": [ 
				"mkdir -p build/unhinted/",
				"python merge.py {}".format(ParamToArgument(param))
			]
		}
		makefile["rule"]["build/noto/{}.otd".format(GenerateFilename(dep["Latin"]))] = {
			"depend": [ "source/noto/{}.ttf".format(GenerateFilename(dep["Latin"])) ],
			"command": [
				"mkdir -p build/noto/",
				"otfccdump --ignore-hints $< -o $@",
			]
		}

	# dump `makefile` dict to actual “GNU Makefile”
	makedump = ""

	for var, val in makefile["variable"].items():
		makedump += "{}={}\n".format(var, val)

	for tar, recipe in makefile["rule"].items():
		dep = recipe["depend"] if "depend" in recipe else []
		makedump += "{}: {}\n".format(tar, " ".join(dep))
		com = recipe["command"] if "command" in recipe else []
		for c in com:
			makedump += "\t{}\n".format(c)

	with codecs.open("Makefile", 'w', 'UTF-8') as mf:
		mf.write(makedump)

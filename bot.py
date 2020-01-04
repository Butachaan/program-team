# -*- coding: utf-8 -*- #

import discord
from discord.ext import commands,tasks
import json
from collections import OrderedDict
import random
import requests
import urllib.request
from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser
import wikipedia
import wikidata.client
from PIL import Image, ImageDraw, ImageFont
import time
import asyncio
import dropbox
import datetime
import pickle
import sys
import platform
import re
from twitter import *
from dateutil.relativedelta import relativedelta as rdelta
import traceback
import threading
import os
import shutil
import pytz
import sqlite3

from operator import itemgetter

#tokens
import config
#cog
import music

"""import logging

logging.basicConfig(level=logging.DEBUG)"""


#トークンたち
DROP_TOKEN = config.DROP_TOKEN
BOT_TEST_TOKEN = config.BOT_TEST_TOKEN
BOT_TOKEN = config.BOT_TOKEN
NAPI_TOKEN = config.NAPI_TOKEN
GAPI_TOKEN = config.GAPI_TOKEN
T_API_key = config.T_API_key
T_API_SKey = config.T_API_SKey
T_Acs_Token = config.T_Acs_Token
T_Acs_SToken = config.T_Acs_SToken

sqlite3.register_converter('pickle', pickle.loads)
sqlite3.register_converter('json', json.loads)
sqlite3.register_adapter(dict, json.dumps)
sqlite3.register_adapter(list, pickle.dumps)
db = sqlite3.connect("sina_datas.db",detect_types=sqlite3.PARSE_DECLTYPES, isolation_level=None)
db.row_factory = sqlite3.Row
cursor = db.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS users(id integer PRIMARY KEY NOT NULL,prefix pickle,gpoint integer,memo json,levcard text,onnotif pickle,lang text,accounts pickle,sinapartner integer,gban integer,gnick text,gcolor integer,gmod integer,gstar integer,galpha integer,gbanhist text)")
cursor.execute("CREATE TABLE IF NOT EXISTS guilds(id integer PRIMARY KEY NOT NULL,levels json,commands json,hash pickle,levelupsendto integer,reward json,jltasks json,lockcom pickle,sendlog integer,prefix pickle,lang text)")
cursor.execute("CREATE TABLE IF NOT EXISTS globalchs(name text PRIMARY KEY NOT NULL,ids pickle)")
cursor.execute("CREATE TABLE IF NOT EXISTS globaldates(id integer PRIMARY KEY NOT NULL,content text,allid pickle,aid integer,gid integer,timestamp text)")

DoServercmd = False
gprofilever = "v1.0.1"
bot = commands.Bot(command_prefix="s-",status=discord.Status.invisible)
bot.owner_id = 404243934210949120
wikipedia.set_lang('ja')
mwc = wikidata.client.Client()
rpcct = 0
rpcs =[
    "ヘルプ:s-help",
    "アイコン:おあずさん",
    "サーバー数:{0}",
    "ユーザー数:{1}",
    "作成:mii-10#3110",
    "help:s-help",
    "icon:oaz_n",
    "{0}guilds",
    "{1}users",
    "created by mii-10#3110"
]
"""db = dropbox.Dropbox(DROP_TOKEN)
db.users_get_current_account()"""
twi = Twitter(auth=OAuth(T_Acs_Token,T_Acs_SToken,T_API_key,T_API_SKey))
ec = 0x42bcf4
Donotif = False
StartTime = datetime.datetime.now() - rdelta(hours=9)
cmdqest = [
    "好きな食べ物は何ですか？",
    "好きな曲は何ですか？",
    "明日世界が終わるとしたら何をしますか？",
    "好きな人がいたとしたらどんな一言をかけたいですか？",
    "お勧めの本はなんですか？",
    "行ってみたい場所はどこですか？",
    "特技は何ですか？",
    "人から依頼されたとき、事情を考えて断れる？断れない？",
    "好きな人は?(公開処刑、もちろん、答えなくてもいいけど",
    "一番欲しいものは？",
]

aglch=None

# gid , oid , invite , PR-text
partnerg=[
    (574170788165582849,404243934210949120,"https://discord.gg/xFHW9tE","""このbot作成者、みぃてん☆の公開サーバーです！
特徴:
・Boost Level 1
  128Kbpsのボイスチャット、720P,60fpsのGoLiveストリームなどを行えます。
・メンバーと新規参加者の徹底的な分離
  メンバー役職が付与されるまでの間、新規参加者は管理者等のみが見れる場でのみ発言できます。荒らしが来てもそこで報告があれば被害を最小限に抑えることができます。
・思惟奈ちゃんによる自動認証
  思惟奈ちゃんのいるサーバーにいるメンバーで、いくつかの条件を満たせば自動認証を受けることができます。いつサーバーに来てもメンバー役職がもらえます。
・相互リンクサーバー
  あなたのサーバーをPR!いくつかの条件を満たすことで相互リンクサーバーになれます。思惟奈ちゃんのパートナーサーバーも兼ねていて、思惟奈ちゃんグローバルチャットにもPR文が流れるようになります！
    """),
    (560434525277126656,404243934210949120,"非公開",""),
    (606583146112352258,452586320053927942,"https://discord.gg/NTU3mar","""ゆったり　まったりしたサーバーを目指しています!!
みなさんのおこしを　おまちしております!!
カラオケのアプリを使ったチャンネルもありますよ!!
よろしくお願いします!!"""),
    (461153681971216384,415526420115095554,"https://discord.gg/hA8bamt","""> **rspnet.jp official**

**rspnet.jp(RisuPu)公式Discordサーバ**
このサーバでは主に マインクラフトサーバへ参加することができたり、自由に雑談・チャットや音楽を自管理botを含めて複数人で別々の音楽が聞くことができます！

詳しい内容は運営までお問い合わせください、又は以下URLを参照してみてね！
https://www.rspnet.jp/page_id=618
    """),
    (648103908170006529,539787492711464960,"https://discord.gg/7P2yVv9","""こちらはYouTubeチャンネル
きゃらちゃんの部屋の公式サーバーです。
リスナーたちが気軽に話せるような場所を提供しております。
是非このサーバーに入ってみませんか？
たくさんの人たちやBotにより安全なサーバーとなっています。
またいち早く動画の通知をゲッドできるチャンスです。
是非入ってくださいね
また、是非チャンネル登録お願いします！
YouTubeチャンネルURL:
https://www.youtube.com/channel/UCPZDqfGwTfWiWhssUArk4ow
    """),
    (641577651022069771,561723377094754304,"https://discord.gg/4JZQAA8","様々なBotもいたり、バラエティに富んだコーナーもあります！")
]

#初回ロード
"""db.files_download_to_file( "guildsetting.json" , "/guildsetting.json" )
db.files_download_to_file( "profiles.json" , "/profiles.json" )
db.files_download_to_file( "gp.json" , "/gp.json" )
db.files_download_to_file( "globaldatas.json" , "/globaldatas.json" )
db.files_download_to_file( "gchatchs.json" , "/gchatchs.json" )"""

tl="　ゔ 、。，．・：；？！゛゜´｀¨＾￣＿ヽヾゝゞ〃仝々〆〇ー―‐／＼～∥｜…‥‘’“”（）〔〕［］｛｝〈〉《》「」『』【】＋－±×÷＝≠＜＞≦≧∞∴♂♀°′″℃￥＄￠￡％＃＆＊＠§☆★○●◎◇◆□■△▲▽▼※〒→←↑↓〓∈∋⊆⊇⊂⊃∪∩∧∨￢⇒⇔∀∃∠⊥⌒∂∇≡≒≪≫√∽∝∵∫∬Å‰♯♭♪†‡¶◯０１２３４５６７８９1234567890ａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚabcdefghijklmnopqrstuvwxyz-^\=~|@[]:;\/.,<>?_+*}{`!\"#$%&'()ぁあぃいぅうぇえぉおかがきぎくぐけげこごさざしじすずせぜそぞただちぢっつづてでとどなにぬねのはばぱひびぴふぶぷへべぺほぼぽまみむめもゃやゅゆょよらりるれろゎわゐゑをんァアィイゥウェエォオカガキギクグケゲコゴサザシジスズセゼソゾタダチヂッツヅテデトドナニヌネノハバパヒビピフブプヘベペホボポマミムメモャヤュユョヨラリルレロヮワヰヱヲンヴヵヶΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩαβγδεζηθικλμνξοπρστυφχψωАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдеёжзийклмнопрстуфхцчшщъыьэюя─│┌┐┘└├┬┤┴┼━┃┏┓┛┗┣┳┫┻╋┠┯┨┷┿┝┰┥┸╂亜唖娃阿哀愛挨姶逢葵茜穐悪握渥旭葦芦鯵梓圧斡扱宛姐虻飴絢綾鮎或粟袷安庵按暗案闇鞍杏以伊位依偉囲夷委威尉惟意慰易椅為畏異移維緯胃萎衣謂違遺医井亥域育郁磯一壱溢逸稲茨芋鰯允印咽員因姻引飲淫胤蔭院陰隠韻吋右宇烏羽迂雨卯鵜窺丑碓臼渦嘘唄欝蔚鰻姥厩浦瓜閏噂云運雲荏餌叡営嬰影映曳栄永泳洩瑛盈穎頴英衛詠鋭液疫益駅悦謁越閲榎厭円園堰奄宴延怨掩援沿演炎焔煙燕猿縁艶苑薗遠鉛鴛塩於汚甥凹央奥往応押旺横欧殴王翁襖鴬鴎黄岡沖荻億屋憶臆桶牡乙俺卸恩温穏音下化仮何伽価佳加可嘉夏嫁家寡科暇果架歌河火珂禍禾稼箇花苛茄荷華菓蝦課嘩貨迦過霞蚊俄峨我牙画臥芽蛾賀雅餓駕介会解回塊壊廻快怪悔恢懐戒拐改魁晦械海灰界皆絵芥蟹開階貝凱劾外咳害崖慨概涯碍蓋街該鎧骸浬馨蛙垣柿蛎鈎劃嚇各廓拡撹格核殻獲確穫覚角赫較郭閣隔革学岳楽額顎掛笠樫橿梶鰍潟割喝恰括活渇滑葛褐轄且鰹叶椛樺鞄株兜竃蒲釜鎌噛鴨栢茅萱粥刈苅瓦乾侃冠寒刊勘勧巻喚堪姦完官寛干幹患感慣憾換敢柑桓棺款歓汗漢澗潅環甘監看竿管簡緩缶翰肝艦莞観諌貫還鑑間閑関陥韓館舘丸含岸巌玩癌眼岩翫贋雁頑顔願企伎危喜器基奇嬉寄岐希幾忌揮机旗既期棋棄機帰毅気汽畿祈季稀紀徽規記貴起軌輝飢騎鬼亀偽儀妓宜戯技擬欺犠疑祇義蟻誼議掬菊鞠吉吃喫桔橘詰砧杵黍却客脚虐逆丘久仇休及吸宮弓急救朽求汲泣灸球究窮笈級糾給旧牛去居巨拒拠挙渠虚許距鋸漁禦魚亨享京供侠僑兇競共凶協匡卿叫喬境峡強彊怯恐恭挟教橋況狂狭矯胸脅興蕎郷鏡響饗驚仰凝尭暁業局曲極玉桐粁僅勤均巾錦斤欣欽琴禁禽筋緊芹菌衿襟謹近金吟銀九倶句区狗玖矩苦躯駆駈駒具愚虞喰空偶寓遇隅串櫛釧屑屈掘窟沓靴轡窪熊隈粂栗繰桑鍬勲君薫訓群軍郡卦袈祁係傾刑兄啓圭珪型契形径恵慶慧憩掲携敬景桂渓畦稽系経継繋罫茎荊蛍計詣警軽頚鶏芸迎鯨劇戟撃激隙桁傑欠決潔穴結血訣月件倹倦健兼券剣喧圏堅嫌建憲懸拳捲検権牽犬献研硯絹県肩見謙賢軒遣鍵険顕験鹸元原厳幻弦減源玄現絃舷言諺限乎個古呼固姑孤己庫弧戸故枯湖狐糊袴股胡菰虎誇跨鈷雇顧鼓五互伍午呉吾娯後御悟梧檎瑚碁語誤護醐乞鯉交佼侯候倖光公功効勾厚口向后喉坑垢好孔孝宏工巧巷幸広庚康弘恒慌抗拘控攻昂晃更杭校梗構江洪浩港溝甲皇硬稿糠紅紘絞綱耕考肯肱腔膏航荒行衡講貢購郊酵鉱砿鋼閤降項香高鴻剛劫号合壕拷濠豪轟麹克刻告国穀酷鵠黒獄漉腰甑忽惚骨狛込此頃今困坤墾婚恨懇昏昆根梱混痕紺艮魂些佐叉唆嵯左差査沙瑳砂詐鎖裟坐座挫債催再最哉塞妻宰彩才採栽歳済災采犀砕砦祭斎細菜裁載際剤在材罪財冴坂阪堺榊肴咲崎埼碕鷺作削咋搾昨朔柵窄策索錯桜鮭笹匙冊刷察拶撮擦札殺薩雑皐鯖捌錆鮫皿晒三傘参山惨撒散桟燦珊産算纂蚕讃賛酸餐斬暫残仕仔伺使刺司史嗣四士始姉姿子屍市師志思指支孜斯施旨枝止死氏獅祉私糸紙紫肢脂至視詞詩試誌諮資賜雌飼歯事似侍児字寺慈持時次滋治爾璽痔磁示而耳自蒔辞汐鹿式識鴫竺軸宍雫七叱執失嫉室悉湿漆疾質実蔀篠偲柴芝屡蕊縞舎写射捨赦斜煮社紗者謝車遮蛇邪借勺尺杓灼爵酌釈錫若寂弱惹主取守手朱殊狩珠種腫趣酒首儒受呪寿授樹綬需囚収周宗就州修愁拾洲秀秋終繍習臭舟蒐衆襲讐蹴輯週酋酬集醜什住充十従戎柔汁渋獣縦重銃叔夙宿淑祝縮粛塾熟出術述俊峻春瞬竣舜駿准循旬楯殉淳準潤盾純巡遵醇順処初所暑曙渚庶緒署書薯藷諸助叙女序徐恕鋤除傷償勝匠升召哨商唱嘗奨妾娼宵将小少尚庄床廠彰承抄招掌捷昇昌昭晶松梢樟樵沼消渉湘焼焦照症省硝礁祥称章笑粧紹肖菖蒋蕉衝裳訟証詔詳象賞醤鉦鍾鐘障鞘上丈丞乗冗剰城場壌嬢常情擾条杖浄状畳穣蒸譲醸錠嘱埴飾拭植殖燭織職色触食蝕辱尻伸信侵唇娠寝審心慎振新晋森榛浸深申疹真神秦紳臣芯薪親診身辛進針震人仁刃塵壬尋甚尽腎訊迅陣靭笥諏須酢図厨逗吹垂帥推水炊睡粋翠衰遂酔錐錘随瑞髄崇嵩数枢趨雛据杉椙菅頗雀裾澄摺寸世瀬畝是凄制勢姓征性成政整星晴棲栖正清牲生盛精聖声製西誠誓請逝醒青静斉税脆隻席惜戚斥昔析石積籍績脊責赤跡蹟碩切拙接摂折設窃節説雪絶舌蝉仙先千占宣専尖川戦扇撰栓栴泉浅洗染潜煎煽旋穿箭線繊羨腺舛船薦詮賎践選遷銭銑閃鮮前善漸然全禅繕膳糎噌塑岨措曾曽楚狙疏疎礎祖租粗素組蘇訴阻遡鼠僧創双叢倉喪壮奏爽宋層匝惣想捜掃挿掻操早曹巣槍槽漕燥争痩相窓糟総綜聡草荘葬蒼藻装走送遭鎗霜騒像増憎臓蔵贈造促側則即息捉束測足速俗属賊族続卒袖其揃存孫尊損村遜他多太汰詑唾堕妥惰打柁舵楕陀駄騨体堆対耐岱帯待怠態戴替泰滞胎腿苔袋貸退逮隊黛鯛代台大第醍題鷹滝瀧卓啄宅托択拓沢濯琢託鐸濁諾茸凧蛸只叩但達辰奪脱巽竪辿棚谷狸鱈樽誰丹単嘆坦担探旦歎淡湛炭短端箪綻耽胆蛋誕鍛団壇弾断暖檀段男談値知地弛恥智池痴稚置致蜘遅馳築畜竹筑蓄逐秩窒茶嫡着中仲宙忠抽昼柱注虫衷註酎鋳駐樗瀦猪苧著貯丁兆凋喋寵帖帳庁弔張彫徴懲挑暢朝潮牒町眺聴脹腸蝶調諜超跳銚長頂鳥勅捗直朕沈珍賃鎮陳津墜椎槌追鎚痛通塚栂掴槻佃漬柘辻蔦綴鍔椿潰坪壷嬬紬爪吊釣鶴亭低停偵剃貞呈堤定帝底庭廷弟悌抵挺提梯汀碇禎程締艇訂諦蹄逓邸鄭釘鼎泥摘擢敵滴的笛適鏑溺哲徹撤轍迭鉄典填天展店添纏甜貼転顛点伝殿澱田電兎吐堵塗妬屠徒斗杜渡登菟賭途都鍍砥砺努度土奴怒倒党冬凍刀唐塔塘套宕島嶋悼投搭東桃梼棟盗淘湯涛灯燈当痘祷等答筒糖統到董蕩藤討謄豆踏逃透鐙陶頭騰闘働動同堂導憧撞洞瞳童胴萄道銅峠鴇匿得徳涜特督禿篤毒独読栃橡凸突椴届鳶苫寅酉瀞噸屯惇敦沌豚遁頓呑曇鈍奈那内乍凪薙謎灘捺鍋楢馴縄畷南楠軟難汝二尼弐迩匂賑肉虹廿日乳入如尿韮任妊忍認濡禰祢寧葱猫熱年念捻撚燃粘乃廼之埜嚢悩濃納能脳膿農覗蚤巴把播覇杷波派琶破婆罵芭馬俳廃拝排敗杯盃牌背肺輩配倍培媒梅楳煤狽買売賠陪這蝿秤矧萩伯剥博拍柏泊白箔粕舶薄迫曝漠爆縛莫駁麦函箱硲箸肇筈櫨幡肌畑畠八鉢溌発醗髪伐罰抜筏閥鳩噺塙蛤隼伴判半反叛帆搬斑板氾汎版犯班畔繁般藩販範釆煩頒飯挽晩番盤磐蕃蛮匪卑否妃庇彼悲扉批披斐比泌疲皮碑秘緋罷肥被誹費避非飛樋簸備尾微枇毘琵眉美鼻柊稗匹疋髭彦膝菱肘弼必畢筆逼桧姫媛紐百謬俵彪標氷漂瓢票表評豹廟描病秒苗錨鋲蒜蛭鰭品彬斌浜瀕貧賓頻敏瓶不付埠夫婦富冨布府怖扶敷斧普浮父符腐膚芙譜負賦赴阜附侮撫武舞葡蕪部封楓風葺蕗伏副復幅服福腹複覆淵弗払沸仏物鮒分吻噴墳憤扮焚奮粉糞紛雰文聞丙併兵塀幣平弊柄並蔽閉陛米頁僻壁癖碧別瞥蔑箆偏変片篇編辺返遍便勉娩弁鞭保舗鋪圃捕歩甫補輔穂募墓慕戊暮母簿菩倣俸包呆報奉宝峰峯崩庖抱捧放方朋法泡烹砲縫胞芳萌蓬蜂褒訪豊邦鋒飽鳳鵬乏亡傍剖坊妨帽忘忙房暴望某棒冒紡肪膨謀貌貿鉾防吠頬北僕卜墨撲朴牧睦穆釦勃没殆堀幌奔本翻凡盆摩磨魔麻埋妹昧枚毎哩槙幕膜枕鮪柾鱒桝亦俣又抹末沫迄侭繭麿万慢満漫蔓味未魅巳箕岬密蜜湊蓑稔脈妙粍民眠務夢無牟矛霧鵡椋婿娘冥名命明盟迷銘鳴姪牝滅免棉綿緬面麺摸模茂妄孟毛猛盲網耗蒙儲木黙目杢勿餅尤戻籾貰問悶紋門匁也冶夜爺耶野弥矢厄役約薬訳躍靖柳薮鑓愉愈油癒諭輸唯佑優勇友宥幽悠憂揖有柚湧涌猶猷由祐裕誘遊邑郵雄融夕予余与誉輿預傭幼妖容庸揚揺擁曜楊様洋溶熔用窯羊耀葉蓉要謡踊遥陽養慾抑欲沃浴翌翼淀羅螺裸来莱頼雷洛絡落酪乱卵嵐欄濫藍蘭覧利吏履李梨理璃痢裏裡里離陸律率立葎掠略劉流溜琉留硫粒隆竜龍侶慮旅虜了亮僚両凌寮料梁涼猟療瞭稜糧良諒遼量陵領力緑倫厘林淋燐琳臨輪隣鱗麟瑠塁涙累類令伶例冷励嶺怜玲礼苓鈴隷零霊麗齢暦歴列劣烈裂廉恋憐漣煉簾練聯蓮連錬呂魯櫓炉賂路露労婁廊弄朗楼榔浪漏牢狼篭老聾蝋郎六麓禄肋録論倭和話歪賄脇惑枠鷲亙亘鰐詫藁蕨椀湾碗腕弌丐丕个丱丶丼丿乂乖乘亂亅豫亊舒弍于亞亟亠亢亰亳亶从仍仄仆仂仗仞仭仟价伉佚估佛佝佗佇佶侈侏侘佻佩佰侑佯來侖儘俔俟俎俘俛俑俚俐俤俥倚倨倔倪倥倅伜俶倡倩倬俾俯們倆偃假會偕偐偈做偖偬偸傀傚傅傴傲僉僊傳僂僖僞僥僭僣僮價僵儉儁儂儖儕儔儚儡儺儷儼儻儿兀兒兌兔兢竸兩兪兮冀冂囘册冉冏冑冓冕冖冤冦冢冩冪冫决冱冲冰况冽凅凉凛几處凩凭凰凵凾刄刋刔刎刧刪刮刳刹剏剄剋剌剞剔剪剴剩剳剿剽劍劔劒剱劈劑辨辧劬劭劼劵勁勍勗勞勣勦飭勠勳勵勸勹匆匈甸匍匐匏匕匚匣匯匱匳匸區卆卅丗卉卍凖卞卩卮夘卻卷厂厖厠厦厥厮厰厶參簒雙叟曼燮叮叨叭叺吁吽呀听吭吼吮吶吩吝呎咏呵咎呟呱呷呰咒呻咀呶咄咐咆哇咢咸咥咬哄哈咨咫哂咤咾咼哘哥哦唏唔哽哮哭哺哢唹啀啣啌售啜啅啖啗唸唳啝喙喀咯喊喟啻啾喘喞單啼喃喩喇喨嗚嗅嗟嗄嗜嗤嗔嘔嗷嘖嗾嗽嘛嗹噎噐營嘴嘶嘲嘸噫噤嘯噬噪嚆嚀嚊嚠嚔嚏嚥嚮嚶嚴囂嚼囁囃囀囈囎囑囓囗囮囹圀囿圄圉圈國圍圓團圖嗇圜圦圷圸坎圻址坏坩埀垈坡坿垉垓垠垳垤垪垰埃埆埔埒埓堊埖埣堋堙堝塲堡塢塋塰毀塒堽塹墅墹墟墫墺壞墻墸墮壅壓壑壗壙壘壥壜壤壟壯壺壹壻壼壽夂夊夐夛梦夥夬夭夲夸夾竒奕奐奎奚奘奢奠奧奬奩奸妁妝佞侫妣妲姆姨姜妍姙姚娥娟娑娜娉娚婀婬婉娵娶婢婪媚媼媾嫋嫂媽嫣嫗嫦嫩嫖嫺嫻嬌嬋嬖嬲嫐嬪嬶嬾孃孅孀孑孕孚孛孥孩孰孳孵學斈孺宀它宦宸寃寇寉寔寐寤實寢寞寥寫寰寶寳尅將專對尓尠尢尨尸尹屁屆屎屓屐屏孱屬屮乢屶屹岌岑岔妛岫岻岶岼岷峅岾峇峙峩峽峺峭嶌峪崋崕崗嵜崟崛崑崔崢崚崙崘嵌嵒嵎嵋嵬嵳嵶嶇嶄嶂嶢嶝嶬嶮嶽嶐嶷嶼巉巍巓巒巖巛巫已巵帋帚帙帑帛帶帷幄幃幀幎幗幔幟幢幤幇幵并幺麼广庠廁廂廈廐廏廖廣廝廚廛廢廡廨廩廬廱廳廰廴廸廾弃弉彝彜弋弑弖弩弭弸彁彈彌彎弯彑彖彗彙彡彭彳彷徃徂彿徊很徑徇從徙徘徠徨徭徼忖忻忤忸忱忝悳忿怡恠怙怐怩怎怱怛怕怫怦怏怺恚恁恪恷恟恊恆恍恣恃恤恂恬恫恙悁悍惧悃悚悄悛悖悗悒悧悋惡悸惠惓悴忰悽惆悵惘慍愕愆惶惷愀惴惺愃愡惻惱愍愎慇愾愨愧慊愿愼愬愴愽慂慄慳慷慘慙慚慫慴慯慥慱慟慝慓慵憙憖憇憬憔憚憊憑憫憮懌懊應懷懈懃懆憺懋罹懍懦懣懶懺懴懿懽懼懾戀戈戉戍戌戔戛戞戡截戮戰戲戳扁扎扞扣扛扠扨扼抂抉找抒抓抖拔抃抔拗拑抻拏拿拆擔拈拜拌拊拂拇抛拉挌拮拱挧挂挈拯拵捐挾捍搜捏掖掎掀掫捶掣掏掉掟掵捫捩掾揩揀揆揣揉插揶揄搖搴搆搓搦搶攝搗搨搏摧摯摶摎攪撕撓撥撩撈撼據擒擅擇撻擘擂擱擧舉擠擡抬擣擯攬擶擴擲擺攀擽攘攜攅攤攣攫攴攵攷收攸畋效敖敕敍敘敞敝敲數斂斃變斛斟斫斷旃旆旁旄旌旒旛旙无旡旱杲昊昃旻杳昵昶昴昜晏晄晉晁晞晝晤晧晨晟晢晰暃暈暎暉暄暘暝曁暹曉暾暼曄暸曖曚曠昿曦曩曰曵曷朏朖朞朦朧霸朮朿朶杁朸朷杆杞杠杙杣杤枉杰枩杼杪枌枋枦枡枅枷柯枴柬枳柩枸柤柞柝柢柮枹柎柆柧檜栞框栩桀桍栲桎梳栫桙档桷桿梟梏梭梔條梛梃檮梹桴梵梠梺椏梍桾椁棊椈棘椢椦棡椌棍棔棧棕椶椒椄棗棣椥棹棠棯椨椪椚椣椡棆楹楷楜楸楫楔楾楮椹楴椽楙椰楡楞楝榁楪榲榮槐榿槁槓榾槎寨槊槝榻槃榧樮榑榠榜榕榴槞槨樂樛槿權槹槲槧樅榱樞槭樔槫樊樒櫁樣樓橄樌橲樶橸橇橢橙橦橈樸樢檐檍檠檄檢檣檗蘗檻櫃櫂檸檳檬櫞櫑櫟檪櫚櫪櫻欅蘖櫺欒欖鬱欟欸欷盜欹飮歇歃歉歐歙歔歛歟歡歸歹歿殀殄殃殍殘殕殞殤殪殫殯殲殱殳殷殼毆毋毓毟毬毫毳毯麾氈氓气氛氤氣汞汕汢汪沂沍沚沁沛汾汨汳沒沐泄泱泓沽泗泅泝沮沱沾沺泛泯泙泪洟衍洶洫洽洸洙洵洳洒洌浣涓浤浚浹浙涎涕濤涅淹渕渊涵淇淦涸淆淬淞淌淨淒淅淺淙淤淕淪淮渭湮渮渙湲湟渾渣湫渫湶湍渟湃渺湎渤滿渝游溂溪溘滉溷滓溽溯滄溲滔滕溏溥滂溟潁漑灌滬滸滾漿滲漱滯漲滌漾漓滷澆潺潸澁澀潯潛濳潭澂潼潘澎澑濂潦澳澣澡澤澹濆澪濟濕濬濔濘濱濮濛瀉瀋濺瀑瀁瀏濾瀛瀚潴瀝瀘瀟瀰瀾瀲灑灣炙炒炯烱炬炸炳炮烟烋烝烙焉烽焜焙煥煕熈煦煢煌煖煬熏燻熄熕熨熬燗熹熾燒燉燔燎燠燬燧燵燼燹燿爍爐爛爨爭爬爰爲爻爼爿牀牆牋牘牴牾犂犁犇犒犖犢犧犹犲狃狆狄狎狒狢狠狡狹狷倏猗猊猜猖猝猴猯猩猥猾獎獏默獗獪獨獰獸獵獻獺珈玳珎玻珀珥珮珞璢琅瑯琥珸琲琺瑕琿瑟瑙瑁瑜瑩瑰瑣瑪瑶瑾璋璞璧瓊瓏瓔珱瓠瓣瓧瓩瓮瓲瓰瓱瓸瓷甄甃甅甌甎甍甕甓甞甦甬甼畄畍畊畉畛畆畚畩畤畧畫畭畸當疆疇畴疊疉疂疔疚疝疥疣痂疳痃疵疽疸疼疱痍痊痒痙痣痞痾痿痼瘁痰痺痲痳瘋瘍瘉瘟瘧瘠瘡瘢瘤瘴瘰瘻癇癈癆癜癘癡癢癨癩癪癧癬癰癲癶癸發皀皃皈皋皎皖皓皙皚皰皴皸皹皺盂盍盖盒盞盡盥盧盪蘯盻眈眇眄眩眤眞眥眦眛眷眸睇睚睨睫睛睥睿睾睹瞎瞋瞑瞠瞞瞰瞶瞹瞿瞼瞽瞻矇矍矗矚矜矣矮矼砌砒礦砠礪硅碎硴碆硼碚碌碣碵碪碯磑磆磋磔碾碼磅磊磬磧磚磽磴礇礒礑礙礬礫祀祠祗祟祚祕祓祺祿禊禝禧齋禪禮禳禹禺秉秕秧秬秡秣稈稍稘稙稠稟禀稱稻稾稷穃穗穉穡穢穩龝穰穹穽窈窗窕窘窖窩竈窰窶竅竄窿邃竇竊竍竏竕竓站竚竝竡竢竦竭竰笂笏笊笆笳笘笙笞笵笨笶筐筺笄筍笋筌筅筵筥筴筧筰筱筬筮箝箘箟箍箜箚箋箒箏筝箙篋篁篌篏箴篆篝篩簑簔篦篥籠簀簇簓篳篷簗簍篶簣簧簪簟簷簫簽籌籃籔籏籀籐籘籟籤籖籥籬籵粃粐粤粭粢粫粡粨粳粲粱粮粹粽糀糅糂糘糒糜糢鬻糯糲糴糶糺紆紂紜紕紊絅絋紮紲紿紵絆絳絖絎絲絨絮絏絣經綉絛綏絽綛綺綮綣綵緇綽綫總綢綯緜綸綟綰緘緝緤緞緻緲緡縅縊縣縡縒縱縟縉縋縢繆繦縻縵縹繃縷縲縺繧繝繖繞繙繚繹繪繩繼繻纃緕繽辮繿纈纉續纒纐纓纔纖纎纛纜缸缺罅罌罍罎罐网罕罔罘罟罠罨罩罧罸羂羆羃羈羇羌羔羞羝羚羣羯羲羹羮羶羸譱翅翆翊翕翔翡翦翩翳翹飜耆耄耋耒耘耙耜耡耨耿耻聊聆聒聘聚聟聢聨聳聲聰聶聹聽聿肄肆肅肛肓肚肭冐肬胛胥胙胝胄胚胖脉胯胱脛脩脣脯腋隋腆脾腓腑胼腱腮腥腦腴膃膈膊膀膂膠膕膤膣腟膓膩膰膵膾膸膽臀臂膺臉臍臑臙臘臈臚臟臠臧臺臻臾舁舂舅與舊舍舐舖舩舫舸舳艀艙艘艝艚艟艤艢艨艪艫舮艱艷艸艾芍芒芫芟芻芬苡苣苟苒苴苳苺莓范苻苹苞茆苜茉苙茵茴茖茲茱荀茹荐荅茯茫茗茘莅莚莪莟莢莖茣莎莇莊荼莵荳荵莠莉莨菴萓菫菎菽萃菘萋菁菷萇菠菲萍萢萠莽萸蔆菻葭萪萼蕚蒄葷葫蒭葮蒂葩葆萬葯葹萵蓊葢蒹蒿蒟蓙蓍蒻蓚蓐蓁蓆蓖蒡蔡蓿蓴蔗蔘蔬蔟蔕蔔蓼蕀蕣蕘蕈蕁蘂蕋蕕薀薤薈薑薊薨蕭薔薛藪薇薜蕷蕾薐藉薺藏薹藐藕藝藥藜藹蘊蘓蘋藾藺蘆蘢蘚蘰蘿虍乕虔號虧虱蚓蚣蚩蚪蚋蚌蚶蚯蛄蛆蚰蛉蠣蚫蛔蛞蛩蛬蛟蛛蛯蜒蜆蜈蜀蜃蛻蜑蜉蜍蛹蜊蜴蜿蜷蜻蜥蜩蜚蝠蝟蝸蝌蝎蝴蝗蝨蝮蝙蝓蝣蝪蠅螢螟螂螯蟋螽蟀蟐雖螫蟄螳蟇蟆螻蟯蟲蟠蠏蠍蟾蟶蟷蠎蟒蠑蠖蠕蠢蠡蠱蠶蠹蠧蠻衄衂衒衙衞衢衫袁衾袞衵衽袵衲袂袗袒袮袙袢袍袤袰袿袱裃裄裔裘裙裝裹褂裼裴裨裲褄褌褊褓襃褞褥褪褫襁襄褻褶褸襌褝襠襞襦襤襭襪襯襴襷襾覃覈覊覓覘覡覩覦覬覯覲覺覽覿觀觚觜觝觧觴觸訃訖訐訌訛訝訥訶詁詛詒詆詈詼詭詬詢誅誂誄誨誡誑誥誦誚誣諄諍諂諚諫諳諧諤諱謔諠諢諷諞諛謌謇謚諡謖謐謗謠謳鞫謦謫謾謨譁譌譏譎證譖譛譚譫譟譬譯譴譽讀讌讎讒讓讖讙讚谺豁谿豈豌豎豐豕豢豬豸豺貂貉貅貊貍貎貔豼貘戝貭貪貽貲貳貮貶賈賁賤賣賚賽賺賻贄贅贊贇贏贍贐齎贓賍贔贖赧赭赱赳趁趙跂趾趺跏跚跖跌跛跋跪跫跟跣跼踈踉跿踝踞踐踟蹂踵踰踴蹊蹇蹉蹌蹐蹈蹙蹤蹠踪蹣蹕蹶蹲蹼躁躇躅躄躋躊躓躑躔躙躪躡躬躰軆躱躾軅軈軋軛軣軼軻軫軾輊輅輕輒輙輓輜輟輛輌輦輳輻輹轅轂輾轌轉轆轎轗轜轢轣轤辜辟辣辭辯辷迚迥迢迪迯邇迴逅迹迺逑逕逡逍逞逖逋逧逶逵逹迸遏遐遑遒逎遉逾遖遘遞遨遯遶隨遲邂遽邁邀邊邉邏邨邯邱邵郢郤扈郛鄂鄒鄙鄲鄰酊酖酘酣酥酩酳酲醋醉醂醢醫醯醪醵醴醺釀釁釉釋釐釖釟釡釛釼釵釶鈞釿鈔鈬鈕鈑鉞鉗鉅鉉鉤鉈銕鈿鉋鉐銜銖銓銛鉚鋏銹銷鋩錏鋺鍄錮錙錢錚錣錺錵錻鍜鍠鍼鍮鍖鎰鎬鎭鎔鎹鏖鏗鏨鏥鏘鏃鏝鏐鏈鏤鐚鐔鐓鐃鐇鐐鐶鐫鐵鐡鐺鑁鑒鑄鑛鑠鑢鑞鑪鈩鑰鑵鑷鑽鑚鑼鑾钁鑿閂閇閊閔閖閘閙閠閨閧閭閼閻閹閾闊濶闃闍闌闕闔闖關闡闥闢阡阨阮阯陂陌陏陋陷陜陞陝陟陦陲陬隍隘隕隗險隧隱隲隰隴隶隸隹雎雋雉雍襍雜霍雕雹霄霆霈霓霎霑霏霖霙霤霪霰霹霽霾靄靆靈靂靉靜靠靤靦靨勒靫靱靹鞅靼鞁靺鞆鞋鞏鞐鞜鞨鞦鞣鞳鞴韃韆韈韋韜韭齏韲竟韶韵頏頌頸頤頡頷頽顆顏顋顫顯顰顱顴顳颪颯颱颶飄飃飆飩飫餃餉餒餔餘餡餝餞餤餠餬餮餽餾饂饉饅饐饋饑饒饌饕馗馘馥馭馮馼駟駛駝駘駑駭駮駱駲駻駸騁騏騅駢騙騫騷驅驂驀驃騾驕驍驛驗驟驢驥驤驩驫驪骭骰骼髀髏髑髓體髞髟髢髣髦髯髫髮髴髱髷髻鬆鬘鬚鬟鬢鬣鬥鬧鬨鬩鬪鬮鬯鬲魄魃魏魍魎魑魘魴鮓鮃鮑鮖鮗鮟鮠鮨鮴鯀鯊鮹鯆鯏鯑鯒鯣鯢鯤鯔鯡鰺鯲鯱鯰鰕鰔鰉鰓鰌鰆鰈鰒鰊鰄鰮鰛鰥鰤鰡鰰鱇鰲鱆鰾鱚鱠鱧鱶鱸鳧鳬鳰鴉鴈鳫鴃鴆鴪鴦鶯鴣鴟鵄鴕鴒鵁鴿鴾鵆鵈鵝鵞鵤鵑鵐鵙鵲鶉鶇鶫鵯鵺鶚鶤鶩鶲鷄鷁鶻鶸鶺鷆鷏鷂鷙鷓鷸鷦鷭鷯鷽鸚鸛鸞鹵鹹鹽麁麈麋麌麒麕麑麝麥麩麸麪麭靡黌黎黏黐黔黜點黝黠黥黨黯黴黶黷黹黻黼黽鼇鼈皷鼕鼡鼬鼾齊齒齔齣齟齠齡齦齧齬齪齷齲齶龕龜龠堯槇遙瑤凜熙"

gguide = """思惟奈ちゃんのグローバルチャット利用規約 最終更新 2019/05/27

1.思惟奈ちゃんグローバルチャット(以下「グローバルチャット」とする)のプロファイルを作成した時点で、この規約に同意したものとする。
2.規約違反者は
  一回目:警告
  二回目:一週間使用禁止
  三回目:永久使用禁止
  を原則とする。使用禁止中に、サブアカウントなどでの禁止回避は判明し次第、メインアカウント、サブアカウントともに永久使用禁止とする。
3.グローバルチャットに、以下のようなテキスト、画像、そのようなコンテンツにつながるURLを投稿することを禁止する。ただし、グローバルチャット作成者、およびグローバルモデレーターは、管理運営に必要な場合は、投稿してもよいとする。
  ・年齢制限の必要なもの
  ・閲覧に金銭や個人情報が必要なもの(ただし、これによって投稿などにログインが必要なサイトのリンク投稿を制限するものではない)
  ・Discordのサーバー招待。ただし新機能のテストのために、「思惟奈ちゃん更新関係サーバー」に誘導する場合など、一部の例外を除く。これによって他のグローバルチャットのグローバルチャンネル名の送信を禁止するものではない。
  ・意味のない文字列の羅列。ただし、接続テストの場合を除く。
  ・その他法律、Discord利用規約に違反するもの
4.グローバルチャット製作者および、グローバルモデレーターは、利用者のできることに加えて、次の行為を行うことができる。
  ・role(肩書)の変更
  (本人からの依頼などの場合。ただし、一部文字列はなりすまし防止のために却下される。)
  ・利用者の使用禁止状態の切り替え
  ・投稿の削除
  上二つの行為を行うのは、前項の項目にある投稿が行われた場合や、製作者、グローバルモデレーターの話し合いの結果、不適切だと判断されたものの場合に限る
5.グローバルチャットにて、ほかのサーバーに送信される項目は、以下のとおりである。
  ・(メッセージの場合)メッセージ内容、付属するembed、添付された画像(ただし一枚のみ)
  ・(リアクションの場合)つけた/外したリアクション
  ・ユーザーのid、投稿時にオフラインでないデバイス(PC,moblie,webの三通り)
  ・送信したサーバーの名前、アイコン、id
  ・送信先のメッセージid一覧
  ・投稿時間
6.この規約は`s-globalguide`でいつでも見ることができる。
7.改定
  ・制作者が予告なしに改定することがある。改定後は、グローバルチャットにて報告される。
  ・予告して改定した場合も、同じように改定後に報告する。
"""

@tasks.loop(minutes=1.0)
async def cRPC():
    global rpcct
    if rpcct==7:
        rpcct=0
    else:
        rpcct=rpcct+1
    await bot.change_presence(status=discord.Status.online,activity=discord.Game(name=rpcs[rpcct].format(len(bot.guilds),len(bot.users))))

def textto(k:str,user):
    if type(user) == str:
        lang = user
        try:
            with open(f"lang/{lang}.json","r",encoding="utf-8") as j:
                f = json.load(j)
        except:
            return f"Not found language:`{lang}`(key:`{k}`)"
        try:
            return f[k]
        except:
            return f"Not found key:`{k}`"
    else:
        cursor.execute("select * from users where id=?",(user.id,))
        upf = cursor.fetchone()
        try:
            cursor.execute("select * from guilds where id=?",(user.guild.id,))
            gpf = cursor.fetchone()
        except:
            gpf={"lang":None}
        lang = upf["lang"]
        if lang is None:
            lang = gpf["lang"]
        if lang is None:
            lang = "ja"
        try:
            with open(f"lang/{lang}.json","r",encoding="utf-8") as j:
                f = json.load(j)
        except:
            return f"Not found language:`{lang}`(key:`{k}`)"
        try:
            return f[k]
        except:
            return f"Not found key:`{k}`"


def getEmbed(ti,desc,color=ec,*optiontext):
    e = discord.Embed(title=ti,description=desc,color=color)
    nmb = -2
    while len(optiontext) >= nmb:
        try:
            nmb = nmb + 2
            e.add_field(name=optiontext[nmb],value=optiontext[nmb+1])
        except IndexError:
            pass
    return e

async def opendm(u):
    dc = u.dm_channel
    if dc == None:
        await u.create_dm()
        dc = u.dm_channel
    return dc

async def repomsg(msg,rs):
    ch = bot.get_channel(628929788421210144)
    e =  discord.Embed(title="グローバルメッセージブロック履歴",description=f"メッセージ内容:{msg.clean_content}",color=ec)
    e.set_author(name=f"{msg.author}(id:{msg.author.id})",icon_url=msg.author.avatar_url_as(static_format="png"))
    e.set_footer(text=f"サーバー:{msg.guild.name}(id:{msg.guild.id})",icon_url=msg.guild.icon_url_as(static_format="png"))
    e.timestamp=msg.created_at
    e.add_field(name="ブロック理由",value=rs or "なし")
    await ch.send(embed=e)

def jfup(j,fpass:str):
    with open(fpass, 'w') as wgp:
        json.dump(j,wgp)
    """with open(fpass,"rb")as spf:
        db.files_upload(spf.read(), f"/{fpass}" ,mode=dropbox.files.WriteMode('overwrite', None))"""

async def gsended(message,ch,embed):
    try:
        tmp = await ch.send(embed=embed)
        
        if not message.embeds[0] == None:
            await ch.send(embed=message.embeds[0])
        return tmp.id
    except:
        pass

async def gsendwh(message,wch,spicon,pf,ed,fls):
    try:
        for wh in await wch.webhooks():
            if wh.name == "sina_global":
                if not fls==[]:
                    sdfl = []
                    for at in fls:
                        sdfl.append(discord.File(f"globalsends/{at.filename}",filename=at.filename,spoiler=at.is_spoiler()))
                    tmp = await wh.send(content=message.clean_content,wait=True,username=f"[{spicon}]{pf['gnick']}", avatar_url=message.author.avatar_url_as(static_format='png'),embeds=ed,files=sdfl)
                else:
                    tmp = await wh.send(content=message.clean_content,wait=True,username=f"[{spicon}]{pf['gnick']}", avatar_url=message.author.avatar_url_as(static_format='png'),embeds=ed)
                return tmp.id
    except:
        pass

async def globalSend(message):
    try:
        cursor.execute("select * from globalchs")
        gchs = cursor.fetchall()
        gchn = None
        for sgch in gchs:
            if message.channel.id in sgch["ids"]:
                gchn = sgch["name"]
                gchs = sgch["ids"]
                break
        if gchn is None:
            return
        if message.content.startswith("//"):
            return
        if message.mention_everyone:
            await repomsg(message,"全員当てメンション")
            return
        if len(message.mentions) >= 5:
            await repomsg(message,"5以上のメンション")
            return
        if message.webhook_id:
            return
        if message.author.id == bot.user.id: 
            return
        cursor.execute("select * from users where id=?",(message.author.id,))
        upf = cursor.fetchone()
        if (datetime.datetime.now() - rdelta(hours=9) - rdelta(days=7) >= message.author.created_at) or upf["gmod"] or upf["gstar"]:
            if upf["gban"] == 1:
                dc=await opendm(message.author)
                await dc.send(textto("global-banned",message.author).format(message.author.mention))
                await repomsg(message,"思惟奈ちゃんグローバルチャットの使用禁止")
                await message.add_reaction("❌")
                await asyncio.sleep(5)
                await message.remove_reaction("❌",bot.user)
            else:
                try:
                    ne = discord.Embed(title="", description="", color=upf["gcolor"])
                    ne.set_author(name=f"{ondevicon(message.author)},ユーザーのID:{str(message.author.id)}")
                    if message.guild.id in [i[0] for i in partnerg]:
                        ne.set_footer(text=f"🔗(パートナーサーバー):{message.guild.name}(id:{message.guild.id})",icon_url=message.guild.icon_url_as(static_format="png"))
                    else:
                        ne.set_footer(text=f"{message.guild.name}(id:{message.guild.id})",icon_url=message.guild.icon_url_as(static_format="png"))
                    ne.timestamp = datetime.datetime.now() - rdelta(hours=9)
                    embed = discord.Embed(title="本文", description=message.content, color=upf["gcolor"])
                    embed.set_footer(text=f"{message.guild.name}(id:{message.guild.id})",icon_url=message.guild.icon_url_as(static_format="png"))
                    if not message.application == None:
                        embed.add_field(name=message.application["name"]+"へのRPC招待", value="RPC招待はグローバル送信できません。")
                    spicon = ""
                    if message.author.id == 404243934210949120:
                        spicon = spicon + "🌈"
                    if message.author.bot:
                        spicon = spicon + "⚙"
                    if upf["sinapartner"]:
                        spicon = spicon + "💠"
                    if message.author.id in [i[1] for i in partnerg]:
                        spicon = spicon + "🔗"
                    if upf["gmod"]:
                        spicon = spicon + "🔧"
                    if upf["galpha"]:
                        spicon = spicon + "🔔"
                    if upf["gstar"]:
                        spicon = spicon + "🌟"
                    if spicon == "":
                        spicon = "👤"
                    embed.set_author(name=f"{upf['gnick']}({spicon}):{str(message.author.id)}", icon_url=message.author.avatar_url_as(static_format="png"))
                    if not message.attachments == []:
                        embed.set_image(url=message.attachments[0].url)
                        for atc in message.attachments:
                            temp = f"{atc.url}\n"
                        embed.add_field(name="添付ファイルのURL一覧", value=temp)
                except:
                    traceback.print_exc(0)
                    await message.add_reaction("❌")
                    await asyncio.sleep(5)
                    await message.remove_reaction("❌",bot.user)
                    return
                try:
                    await message.add_reaction(bot.get_emoji(653161518346534912))
                except:
                    pass
            if gchn.startswith("ed-"):
                tasks=[]
                for cid in gchs:
                    ch = bot.get_channel(cid)
                    tasks.append(asyncio.ensure_future(gsended(message,ch,embed)))
                cursor.execute("select * from globalchs where name=?",(gchn.replace("ed-",""),))
                nch = cursor.fetchone()
                try:
                    if nch["ids"]:
                        for cid in nch["ids"]:
                            try:
                                if not cid == message.channel.id:
                                    wch = bot.get_channel(cid)
                                    tasks.append(asyncio.ensure_future(gsendwh(message,wch,spicon,upf,ne,[])))
                            except:
                                pass
                    mids = await asyncio.gather(*tasks)
                    if message.attachments == []:
                        await message.delete()
                except:
                    pass
                try:
                    await message.remove_reaction(bot.get_emoji(653161518346534912),bot.user)
                except:
                    pass
            else:
                try:
                    sfs = False
                    fls = []
                    ed = []
                    if not message.attachments == []:
                        os.makedirs('globalsends/', exist_ok=True)
                        for at in message.attachments:
                            await at.save(f"globalsends/{at.filename}")
                            fls.append(at)
                        ed = ed + message.embeds + [ne]
                    else:
                        ed = ed + message.embeds + [ne]
                except:
                    traceback.print_exc(0)
                    await message.add_reaction("❌")
                    await asyncio.sleep(5)
                    await message.remove_reaction("❌",bot.user)
                    return
                try:
                    await message.add_reaction(bot.get_emoji(653161518346534912))
                except:
                    pass
                tasks = []
                for cid in gchs:
                    try:
                        if not cid == message.channel.id:
                            wch = bot.get_channel(cid)
                            tasks.append(asyncio.ensure_future(gsendwh(message,wch,spicon,upf,ed,fls)))
                    except:
                        pass
                cursor.execute("select * from globalchs where name=?",(f"ed-{gchn}",))
                och = cursor.fetchone()
                try:
                    if nch["ids"]:
                        for cid in och["ids"]:
                            ch = bot.get_channel(cid)
                            tasks.append(asyncio.ensure_future(gsended(message,ch,embed)))
                except:
                    pass
                    mids = await asyncio.gather(*tasks)

                if not fls == []:
                    shutil.rmtree("globalsends/")
                try:
                    await message.remove_reaction(bot.get_emoji(653161518346534912),bot.user)
                except:
                    pass
            cursor.execute("INSERT INTO globaldates(id,content,allid,aid,gid,timestamp) VALUES(?,?,?,?,?,?)", (int(time.time())+random.randint(1,30),message.clean_content,mids+[message.id],message.author.id,message.guild.id,str(message.created_at)))        
            await message.add_reaction(bot.get_emoji(653161518195539975))
            await asyncio.sleep(5)
            await message.remove_reaction(bot.get_emoji(653161518195539975),bot.user)
        else:
            await repomsg(message,"作成後7日に満たないアカウント")
    except Exception as e:
        traceback.print_exc()

@bot.event
async def on_voice_state_update(member, before, after):
    try:
        if [i for i in member.guild.me.voice.channel.members if not i.bot]==[]:
            await member.guild.voice_client.disconnect()
    except:
        pass
    try:
        if bot.voice_clients == []:
            shutil.rmtree("musicfile/")
            os.makedirs('musicfile/', exist_ok=True)
    except:
        pass

@bot.event
async def on_member_update(b,a):
    global Donotif
    #serverlog
    try:
        e=discord.Embed(title="メンバーの更新",description=f"変更メンバー:{str(a)}",color=ec)
        e.timestamp = datetime.datetime.now() - rdelta(hours=9)
        if not b.nick == a.nick:
            e.add_field(name="変更内容",value="ニックネーム")
            if b.nick:
                bnick = b.nick
            else:
                bnick = b.name
            if a.nick:
                anick = a.nick
            else:
                anick = a.name
            e.add_field(name="変更前",value=bnick.replace("\\","\\\\").replace("*","\*").replace("_","\_").replace("|","\|").replace("~","\~").replace("`","\`").replace(">","\>"))
            e.add_field(name="変更後",value=anick.replace("\\","\\\\").replace("*","\*").replace("_","\_").replace("|","\|").replace("~","\~").replace("`","\`").replace(">","\>"))
            cursor.execute("select * from guilds where id=?",(a.guild.id,))
            gpf = cursor.fetchone()
            if gpf["sendlog"]:
                ch = bot.get_channel(gpf["sendlog"])
                if ch.guild.id == a.guild.id:
                    await ch.send(embed=e)
        elif not b.roles == a.roles:
            if len(b.roles) > len(a.roles):
                e.add_field(name="変更内容",value="役職除去")
                e.add_field(name="役職",value=list(set(b.roles)-set(a.roles))[0])
            else:
                e.add_field(name="変更内容",value="役職付与")
                e.add_field(name="役職",value=list(set(a.roles)-set(b.roles))[0])
            cursor.execute("select * from guilds where id=?",(a.guild.id,))
            gpf = cursor.fetchone()
            if gpf["sendlog"]:
                ch = bot.get_channel(gpf["sendlog"])
                if ch.guild.id == a.guild.id:
                    await ch.send(embed=e)
            e.set_footer(text=a.guild.name,icon_url=a.guild.icon_url_as(static_format="png"))
            e.timestamp = datetime.datetime.now() - rdelta(hours=9)
            await aglch.send(embed=e)
    except:
        pass
    while Donotif:
        await asyncio.sleep(0.5)
    Donotif = True
    cursor.execute("select * from users")
    upf = cursor.fetchall()
    try:
        if str(b.status)=="offline" and not str(a.status)=="offline":
            for pf in upf:
                if a.id in pf["onnotif"] :
                    sdu = bot.get_user(pf["id"])
                    dc = await opendm(sdu)
                    lm = await dc.history(limit=1).flatten()
                    nf=str(bot.get_emoji(653161518531215390))+textto("onlinenotif",sdu).format(str(a)).replace(str(bot.get_user(455284639108431873))+"さん","おあずちゃん").replace(str(bot.get_user(404243934210949120)),"みぃてん☆")
                    if not lm[0].content==nf:
                        ts = discord.Embed(title="", description="", color=ec)
                        ts.set_footer(text=ondevicon(a)+","+textto("sendedat",sdu))
                        ts.timestamp = datetime.datetime.now() - rdelta(hours=9)
                        await dc.send(nf,embed=ts)
        elif not str(b.status)=="offline" and str(a.status)=="offline":
            for pf in upf:
                if a.id in pf["onnotif"]:
                    sdu = bot.get_user(pf["id"])
                    dc = await opendm(sdu)
                    lm = await dc.history(limit=1).flatten()
                    nf=str(bot.get_emoji(653161518392803348))+textto("offlinenotif",sdu).format(str(a)).replace(str(bot.get_user(455284639108431873))+"さん","おあずちゃん").replace(str(bot.get_user(404243934210949120)),"みぃてん☆")
                    if not lm[0].content==nf:
                        ts = discord.Embed(title="", description="", color=ec)
                        ts.set_footer(text=textto("sendedat",sdu))
                        ts.timestamp = datetime.datetime.now() - rdelta(hours=9)
                        await dc.send(nf,embed=ts)
    except:
        print(traceback.format_exc(2))
    Donotif = False

async def nga(m,r):
    ch=m.guild.get_channel(631875590307446814)
    
    admins = m.guild.get_role(574494236951707668)
    tmpadmins = m.guild.get_role(583952666317684756)
    subadmins = m.guild.get_role(579283058394660864)
    giverole = m.guild.get_role(620911942889897984)
    tch = await ch.create_text_channel(f"認証待ち-{m.name}",overwrites={
        m:discord.PermissionOverwrite(read_messages=True,send_messages=True),
        m.guild.default_role:discord.PermissionOverwrite(read_messages=False),
        admins:discord.PermissionOverwrite(read_messages=True,send_messages=True),
        tmpadmins:discord.PermissionOverwrite(read_messages=True,send_messages=True),
        subadmins:discord.PermissionOverwrite(read_messages=True,send_messages=True),
        giverole:discord.PermissionOverwrite(read_messages=True,send_messages=True)
    },topic=str(m.id))
    await tch.send(f"""{m.mention}さん！みぃてん☆の公開サーバー(以下「このサーバー」)にようこそ！
あなたは{r}が理由で、試験運用中の自動認証が行われませんでした。
まずはルールを確認してください!
https://gist.github.com/apple502j/1a81b1a95253609f0c67ecb74f38754b
その後、そのことを報告してください。その後に決定されるまでに、いくつか質問する場合があります。また、あなたの方の質問も、この場を使って行ってください。
    """)

@bot.event
async def on_member_join(member):
    if member.guild.id == 574170788165582849:
        if member.bot:
            await member.add_roles(member.guild.get_role(574494559946539009))
        else:
            uich = bot.get_channel(633651383353999370)
            
            e= discord.Embed(title=f"参加メンバー{member}について",color=ec)
            e.add_field(name="共通サーバー数",value=len([g for g in bot.guilds if g.get_member(member.id)]))
            e.add_field(name="ID",value=member.id)
            e.set_footer(text="アカウント作成タイムスタンプ")
            e.timestamp=member.created_at
            await uich.send(embed=e)
            mrole = member.guild.get_role(574494088837988352)
            
            bunotif = 0
            if len([g for g in bot.guilds if g.get_member(member.id)]) == 1:
                await nga(member,"思惟奈ちゃんとの共通のサーバーがほかにないこと")
            else:
                for g in bot.guilds:
                    
                    try:
                        tmp = await g.bans()
                    except:
                        continue
                    banulist = [i.user.id for i in tmp]
                    if member.id in banulist:
                        bunotif = bunotif + 1
                if bunotif != 0:
                    await nga(member,"思惟奈ちゃんとの共通のほかサーバーでのban")
                    pass
                else:
                    if datetime.datetime.now() - rdelta(hours=9) - rdelta(days=7) < member.created_at:
                        await nga(member,"アカウントの作成から7日経過していないこと")
                        pass
                    else:
                        await member.add_roles(mrole)
                        ch = await opendm(member)
                        try:
                            await ch.send(f"""{member.mention}さん！みぃてん☆の公開サーバー(以下「このサーバー」)にようこそ！
    あなたは、いくつかの条件を満たしているため、自動的に役職が付与されましたので、サーバーで、ゆっくり過ごされて行ってください。
    ですが、使用前にまずはルールを確認してください!
    https://gist.github.com/apple502j/1a81b1a95253609f0c67ecb74f38754b
    また、必要に応じて通知設定を「すべてのメッセージ」などに変更してください。(デフォルトは「@メンションのみ」です。)
                            """)
                        except:
                            ch = member.guild.get_channel(574494906287128577)
                            await ch.send(f"""{member.mention}さん！みぃてん☆の公開サーバー(以下「このサーバー」)にようこそ！
    あなたは、いくつかの条件を満たしているため、自動的に役職が付与されましたので、サーバーで、ゆっくり過ごされて行ってください。
    ですが、使用前にまずはルールを確認してください!
    https://gist.github.com/apple502j/1a81b1a95253609f0c67ecb74f38754b
    また、必要に応じて通知設定を「すべてのメッセージ」などに変更してください。(デフォルトは「@メンションのみ」です。)
                            """)
                        schs=[631815290044284938,574494906287128577]
                        for c in schs:
                            
                            sch = bot.get_channel(c)
                            await sch.send(embed=getEmbed("自動認証(試験運用中)完了のお知らせ",f"{member.mention}さんが自動認証を済ませました。"))
    else:
        try:
            cursor.execute("select * from guilds where id=?",(member.guild.id,))
            gpf = cursor.fetchone()
            ctt = gpf["jltasks"]
            if not ctt.get("welcome") == None:
                if ctt["welcome"]["sendto"] == "sysch":
                    await member.guild.system_channel.send(ctt["welcome"]["content"].format(member.mention))
                else:
                    dc = await opendm(member)
                    await dc.send(ctt["welcome"]["content"].format(member.mention))
        except:
            pass
    e=discord.Embed(title="メンバーの参加",description=f"{len(member.guild.members)}人目のメンバー",color=ec)
    e.add_field(name="参加メンバー",value=member.mention)
    e.add_field(name="そのユーザーのid",value=member.id)
    e.set_footer(text=f"アカウント作成日時(そのままの値:{member.created_at},タイムスタンプ化:")
    e.timestamp = member.created_at
    cursor.execute("select * from guilds where id=?",(member.guild.id,))
    gpf = cursor.fetchone()
    if gpf["sendlog"]:
        ch = bot.get_channel(gpf["sendlog"])
        if ch.guild.id == member.guild.id:
            await ch.send(embed=e)
    e.set_footer(text=member.guild.name,icon_url=member.guild.icon_url_as(static_format="png"))
    e.timestamp = datetime.datetime.now() - rdelta(hours=9)
    await aglch.send(embed=e)
    #他サーバーでのban通知
    bunotif = 0
    for g in bot.guilds:
        
        try:
            tmp = await g.bans()
        except:
            continue
        banulist = [i.user.id for i in tmp]
        if member.id in banulist:
            bunotif = bunotif + 1
    if bunotif == 0:
        for ch in member.guild.channels:
            if ch.name == "sina-user-check":
                await ch.send(embed=discord.Embed(title=f"{member}の安全性評価",description=f"そのユーザーは、思惟奈ちゃんのいるサーバーでは、banされていません。"))
    else:
        for ch in member.guild.channels:
            if ch.name == "sina-user-check":
                await ch.send(embed=discord.Embed(title=f"{member}の安全性評価",description=f"そのユーザーは、思惟奈ちゃんのいる{bunotif}のサーバーでbanされています。注意してください。"))


@bot.event
async def on_member_remove(member):
    if member.guild.id == 574170788165582849:
        await member.guild.system_channel.send(f"{str(member)}さんがこのサーバーを退出しました。")
    else:
        try:
            cursor.execute("select * from guilds where id=?",(member.guild.id,))
            gpf = cursor.fetchone()
            ctt = gpf["jltasks"]
            if not ctt.get("cu") == None:
                if ctt["cu"]["sendto"] == "sysch":
                    await member.guild.system_channel.send(ctt["cu"]["content"].format(str(member)))
                else:
                    dc = await opendm(member)
                    await dc.send(ctt["cu"]["content"].format(str(member)))
        except:
            pass
    e=discord.Embed(title="メンバーの退出",color=ec)
    e.add_field(name="退出メンバー",value=str(member))
    e.add_field(name="役職",value=[i.name for i in member.roles])
    #e.set_footer(text=f"{member.guild.name}/{member.guild.id}")
    e.timestamp = datetime.datetime.now() - rdelta(hours=9)
    cursor.execute("select * from guilds where id=?",(member.guild.id,))
    gpf = cursor.fetchone()
    if gpf["sendlog"]:
        ch = bot.get_channel(gpf["sendlog"])
        if ch.guild.id == member.guild.id:
            await ch.send(embed=e)
    e.set_footer(text=member.guild.name,icon_url=member.guild.icon_url_as(static_format="png"))
    e.timestamp = datetime.datetime.now() - rdelta(hours=9)
    await aglch.send(embed=e)
    """if member.guild.id == 611445741902364672:
        c = bot.get_channel(613629308166209549)
        await c.send(embed=e)"""

@bot.event
async def on_webhooks_update(channel):
    e=discord.Embed(title="Webhooksの更新",color=ec)
    e.add_field(name="チャンネル",value=channel.mention)
    e.timestamp = datetime.datetime.now() - rdelta(hours=9)
    cursor.execute("select * from guilds where id=?",(channel.guild.id,))
    gpf = cursor.fetchone()
    if gpf["sendlog"]:
        ch = bot.get_channel(gpf["sendlog"])
        if ch.guild.id == channel.guild.id:
            await ch.send(embed=e)
    e.set_footer(text=channel.guild.name,icon_url=channel.guild.icon_url_as(static_format="png"))
    e.timestamp = datetime.datetime.now() - rdelta(hours=9)
    await aglch.send(embed=e)

@bot.event
async def on_guild_role_create(role):
    e=discord.Embed(title="役職の作成",color=ec)
    e.add_field(name="役職名",value=role.name)
    e.timestamp = datetime.datetime.now() - rdelta(hours=9)
    cursor.execute("select * from guilds where id=?",(role.guild.id,))
    gpf = cursor.fetchone()
    if gpf["sendlog"]:
        ch = bot.get_channel(gpf["sendlog"])
        if ch.guild.id == role.guild.id:
            await ch.send(embed=e)
    e.set_footer(text=role.guild.name,icon_url=role.guild.icon_url_as(static_format="png"))
    e.timestamp = datetime.datetime.now() - rdelta(hours=9)
    await aglch.send(embed=e)

@bot.event
async def on_guild_role_delete(role):
    e=discord.Embed(title="役職の削除",color=ec)
    e.add_field(name="役職名",value=role.name)
    e.timestamp = datetime.datetime.now() - rdelta(hours=9)
    cursor.execute("select * from guilds where id=?",(role.guild.id,))
    gpf = cursor.fetchone()
    if gpf["sendlog"]:
        ch = bot.get_channel(gpf["sendlog"])
        if ch.guild.id == role.guild.id:
            await ch.send(embed=e)
    e.set_footer(text=role.guild.name,icon_url=role.guild.icon_url_as(static_format="png"))
    e.timestamp = datetime.datetime.now() - rdelta(hours=9)
    await aglch.send(embed=e)

@bot.event
async def on_message_edit(before, after):
    if not after.author.bot:
        if before.content != after.content:
            e=discord.Embed(title="メッセージの編集",color=ec)
            e.add_field(name="編集前",value=before.content)
            e.add_field(name="編集後",value=after.content)
            e.add_field(name="メッセージ送信者",value=after.author.mention)
            e.add_field(name="メッセージチャンネル",value=after.channel.mention)
            e.add_field(name="メッセージのURL",value=after.jump_url)
            e.timestamp = datetime.datetime.now() - rdelta(hours=9)
            cursor.execute("select * from guilds where id=?",(after.guild.id,))
            gpf = cursor.fetchone()
            if gpf["sendlog"]:
                ch = bot.get_channel(gpf["sendlog"])
                if ch.guild.id == after.guild.id:
                    await ch.send(embed=e) 
            e.set_footer(text=after.guild.name,icon_url=after.guild.icon_url_as(static_format="png"))
            e.timestamp = datetime.datetime.now() - rdelta(hours=9)
            await aglch.send(embed=e)

@bot.event
async def on_guild_channel_delete(channel):
    bl=await channel.guild.audit_logs(limit=1,action=discord.AuditLogAction.channel_delete).flatten()
    e=discord.Embed(title="チャンネル削除",color=ec)
    e.add_field(name="チャンネル名",value=channel.name)
    e.timestamp = datetime.datetime.now() - rdelta(hours=9)
    cursor.execute("select * from guilds where id=?",(channel.guild.id,))
    gpf = cursor.fetchone()
    if gpf["sendlog"]:
        ch = bot.get_channel(gpf["sendlog"])
        if ch.guild.id == channel.guild.id:
            await ch.send(embed=e)
    e.set_footer(text=channel.guild.name,icon_url=channel.guild.icon_url_as(static_format="png"))
    e.timestamp = datetime.datetime.now() - rdelta(hours=9)
    await aglch.send(embed=e)

@bot.event
async def on_reaction_clear(message, reactions):
    e=discord.Embed(title="リアクションの一斉除去",color=ec)
    e.add_field(name="リアクション",value=[str(i) for i in reactions])
    e.add_field(name="除去されたメッセージ",value=message.content or "(本文なし)")
    e.timestamp = datetime.datetime.now() - rdelta(hours=9)
    cursor.execute("select * from guilds where id=?",(message.guild.id,))
    gpf = cursor.fetchone()
    if gpf["sendlog"]:
        ch = bot.get_channel(gpf["sendlog"])
        if ch.guild.id == message.guild.id:
            await ch.send(embed=e)
    e.set_footer(text=message.guild.name,icon_url=message.guild.icon_url_as(static_format="png"))
    e.timestamp = datetime.datetime.now() - rdelta(hours=9)
    await aglch.send(embed=e)

@bot.event
async def on_message_delete(message):
    if not message.author.bot:
        e=discord.Embed(title="メッセージ削除",color=ec)
        e.add_field(name="メッセージ",value=message.content)
        e.add_field(name="メッセージ送信者",value=message.author.mention)
        e.add_field(name="メッセージチャンネル",value=message.channel.mention)
        e.add_field(name="メッセージのid",value=message.id)
        e.timestamp = datetime.datetime.now() - rdelta(hours=9)
        cursor.execute("select * from guilds where id=?",(message.guild.id,))
        gpf = cursor.fetchone()
        if gpf["sendlog"]:
            ch = bot.get_channel(gpf["sendlog"])
            if ch.guild.id == message.guild.id:
                await ch.send(embed=e)
        e.set_footer(text=message.guild.name,icon_url=message.guild.icon_url_as(static_format="png"))
        e.timestamp = datetime.datetime.now() - rdelta(hours=9)
        await aglch.send(embed=e)


@bot.event
async def on_bulk_message_delete(messages):
    e=discord.Embed(title="メッセージ一括削除",color=ec)
    e.add_field(name="件数",value=len(messages))
    e.timestamp = datetime.datetime.now() - rdelta(hours=9)
    for message in messages:
        if not message.author.bot:
            e.add_field(name="メッセージ",value=message.content)
            e.add_field(name="メッセージ送信者",value=message.author.mention)
            e.add_field(name="メッセージのid",value=message.id)
    cursor.execute("select * from guilds where id=?",(messages[0].guild.id,))
    gpf = cursor.fetchone()
    if gpf["sendlog"]:
        ch = bot.get_channel(gpf["sendlog"])
        if ch.guild.id == messages[0].guild.id:
            await ch.send(embed=e)
    e.set_footer(text=messages[0].guild.name,icon_url=messages[0].guild.icon_url_as(static_format="png"))
    e.timestamp = datetime.datetime.now() - rdelta(hours=9)
    await aglch.send(embed=e)


@bot.event
async def on_guild_channel_create(channel):
    e=discord.Embed(title="チャンネル作成",color=ec)
    e.add_field(name="チャンネル名",value=channel.mention)
    e.timestamp = datetime.datetime.now() - rdelta(hours=9)
    cursor.execute("select * from guilds where id=?",(channel.guild.id,))
    gpf = cursor.fetchone()
    if gpf["sendlog"]:
        ch = bot.get_channel(gpf["sendlog"])
        if ch.guild.id == channel.guild.id:
            await ch.send(embed=e)
    e.set_footer(text=channel.guild.name,icon_url=channel.guild.icon_url_as(static_format="png"))
    e.timestamp = datetime.datetime.now() - rdelta(hours=9)
    await aglch.send(embed=e)

@bot.event
async def on_guild_channel_update(b, a):
    e=discord.Embed(title="チャンネル更新",description=a.mention,color=ec)
    e.timestamp = datetime.datetime.now() - rdelta(hours=9)
    if not b.name == a.name:
        if not a.guild.id == 461789442743468073:
            e.add_field(name="変更内容",value="チャンネル名")
            e.add_field(name="変更前",value=b.name)
            e.add_field(name="変更後",value=a.name)
            cursor.execute("select * from guilds where id=?",(a.guild.id,))
            gpf = cursor.fetchone()
            if gpf["sendlog"]:
                ch = bot.get_channel(gpf["sendlog"])
                if ch.guild.id == a.guild.id:
                    await ch.send(embed=e)
            e.set_footer(text=a.guild.name,icon_url=a.guild.icon_url_as(static_format="png"))
            e.timestamp = datetime.datetime.now() - rdelta(hours=9)
            await aglch.send(embed=e)
    elif not b.changed_roles == a.changed_roles:
        e.add_field(name="変更内容",value="権限の上書き")
        e.add_field(name="確認:",value="チャンネル設定を見てください。")
        cursor.execute("select * from guilds where id=?",(a.guild.id,))
        gpf = cursor.fetchone()
        if gpf["sendlog"]:
            ch = bot.get_channel(gpf["sendlog"])
            if ch.guild.id == a.guild.id:
                await ch.send(embed=e)    
        e.set_footer(text=a.guild.name,icon_url=a.guild.icon_url_as(static_format="png"))
        e.timestamp = datetime.datetime.now() - rdelta(hours=9)
        await aglch.send(embed=e)
    elif isinstance(b,discord.TextChannel):
        if not b.topic == a.topic:
            e.add_field(name="変更内容",value="チャンネルトピック")
            e.add_field(name="変更前",value=b.topic)
            e.add_field(name="変更後",value=a.topic)
            cursor.execute("select * from guilds where id=?",(a.guild.id,))
            gpf = cursor.fetchone()
            if gpf["sendlog"]:
                ch = bot.get_channel(gpf["sendlog"])
                if ch.guild.id == a.guild.id:
                    await ch.send(embed=e)
            e.set_footer(text=a.guild.name,icon_url=a.guild.icon_url_as(static_format="png"))
            e.timestamp = datetime.datetime.now() - rdelta(hours=9)
            await aglch.send(embed=e)

@bot.event
async def on_guild_update(b, a):
    e=discord.Embed(title="サーバーの更新",color=ec)
    e.timestamp = datetime.datetime.now() - rdelta(hours=9)
    if b.name != a.name:
        e.add_field(name="変更内容",value="サーバー名")
        e.add_field(name="変更前",value=b.name)
        e.add_field(name="変更後",value=a.name)
        cursor.execute("select * from guilds where id=?",(a.id,))
        gpf = cursor.fetchone()
        if gpf["sendlog"]:
            ch = bot.get_channel(gpf["sendlog"])
            if ch.guild.id == a.id:
                await ch.send(embed=e)
        e.set_footer(text=a.name,icon_url=a.icon_url_as(static_format="png"))
        e.timestamp = datetime.datetime.now() - rdelta(hours=9)
        await aglch.send(embed=e)
    elif b.icon != a.icon:
        e.add_field(name="変更内容",value="サーバーアイコン")
        cursor.execute("select * from guilds where id=?",(a.id,))
        gpf = cursor.fetchone()
        if gpf["sendlog"]:
            ch = bot.get_channel(gpf["sendlog"])
            if ch.guild.id == a.id:
                await ch.send(embed=e)
        e.set_footer(text=a.name,icon_url=a.icon_url_as(static_format="png"))
        e.timestamp = datetime.datetime.now() - rdelta(hours=9)
        await aglch.send(embed=e)
    elif b.owner.id != a.owner.id:
        e.add_field(name="変更内容",value="サーバー所有者の変更")
        e.add_field(name="変更前",value=b.owner)
        e.add_field(name="変更後",value=a.owner)
        cursor.execute("select * from guilds where id=?",(a.id,))
        gpf = cursor.fetchone()
        if gpf["sendlog"]:
            ch = bot.get_channel(gpf["sendlog"])
            if ch.guild.id == a.id:
                await ch.send(embed=e)
        e.set_footer(text=a.name,icon_url=a.icon_url_as(static_format="png"))
        e.timestamp = datetime.datetime.now() - rdelta(hours=9)
        await aglch.send(embed=e)

@bot.event
async def on_member_ban(g, user):
    guild = bot.get_guild(g.id)
    bl=await guild.audit_logs(limit=1,action=discord.AuditLogAction.ban).flatten()
    e=discord.Embed(title="ユーザーのban",color=ec)
    e.add_field(name="ユーザー名",value=str(user))
    e.add_field(name="(テスト)実行者",value=str(bl[0].user))
    #e.set_footer(text=f"{g.name}/{g.id}")
    e.timestamp = datetime.datetime.now() - rdelta(hours=9)
    cursor.execute("select * from guilds where id=?",(g.id,))
    gpf = cursor.fetchone()
    if gpf["sendlog"]:
        ch = bot.get_channel(gpf["sendlog"])
        if ch.guild.id == g.id:
            await ch.send(embed=e)
    e.set_footer(text=g.name,icon_url=g.icon_url_as(static_format="png"))
    e.timestamp = datetime.datetime.now() - rdelta(hours=9)
    await aglch.send(embed=e)
    """if g.id == 611445741902364672:
        c = bot.get_channel(613629308166209549)
        await c.send(embed=e)"""

@bot.event
async def on_member_unban(guild, user):
    e=discord.Embed(title="ユーザーのban解除",color=ec)
    e.add_field(name="ユーザー名",value=str(user))
    e.timestamp = datetime.datetime.now() - rdelta(hours=9)
    cursor.execute("select * from guilds where id=?",(guild.id,))
    gpf = cursor.fetchone()
    if gpf["sendlog"]:
        ch = bot.get_channel(gpf["sendlog"])
        if ch.guild.id == guild.id:
            await ch.send(embed=e)
    e.set_footer(text=guild.name,icon_url=guild.icon_url_as(static_format="png"))
    e.timestamp = datetime.datetime.now() - rdelta(hours=9)
    await aglch.send(embed=e)

@bot.event
async def on_guild_join(guild):
    dc = await opendm(bot.get_user(404243934210949120))
    await dc.send(f"`{guild.name}`(id:{guild.id})に参加しました。")

@bot.event
async def on_guild_remove(guild):
    dc = await opendm(bot.get_user(404243934210949120))
    await dc.send(f"`{guild.name}`(id:{guild.id})から退出しました。")

@bot.event
async def on_guild_channel_pins_update(ch,lmtime):
    if ch.guild.id in [461153681971216384,574170788165582849]:
        await ch.send(embed=getEmbed("pin-update!","",ec))

@bot.event
async def on_ready():
    global aglch
    print('ログインしました。')
    print(bot.user.name)
    print(bot.user.id)
    print('------------------')
    try:
        ch = bot.get_channel(595526013031546890)
        await ch.send(f"{bot.get_emoji(653161518531215390)}起動完了！")
    except:
        pass
    aglch = bot.get_channel(659706303521751072)
    cRPC.start()
    invite_tweet.start()
    now_sina_tweet.start()
    bot.load_extension("jishaku")
    music.setup(bot)

@bot.event
async def on_message(message):
    if isinstance(message.channel,discord.DMChannel):
        return
    if message.author.id==bot.user.id:
        return
    #db.files_download_to_file( "guildsetting.json" , "/guildsetting.json" )
    #db.files_download_to_file( "profiles.json" , "/profiles.json" )
    tks=[
        asyncio.ensure_future(domsg(message)),
        asyncio.ensure_future(globalSend(message)),
    ]
    await asyncio.gather(*tks)


async def domsg(message):
    global DoServercmd
    cursor.execute("select * from users where id=?",(message.author.id,))
    upf = cursor.fetchone()
    if not upf:
        cursor.execute("INSERT INTO users(id,prefix,gpoint,memo,levcard,onnotif,lang,accounts,sinapartner,gban,gnick,gcolor,gmod,gstar,galpha,gbanhist) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", (message.author.id,[],0,{},"m@ji☆",[],None,[],0,0,message.author.name,0,0,0,0,"なし"))
        try:
            dc=await opendm(message.author)
            await dc.send(f"{bot.get_emoji(653161518153596950)}あなたの思惟奈ちゃんユーザープロファイルを作成しました！いくつかの項目はコマンドを使って書き換えることができます。詳しくはヘルプ(`s-help`)をご覧ください。\n以前からの利用者へ:様々な設定がリセットされています。再設定をお願いします。また、不具合がありましたら`mii-10#3110`にお願いします。")
        except:
            pass
    cursor.execute("select * from users where id=?",(message.author.id,))
    pf = cursor.fetchone()

    cursor.execute("select * from guilds where id=?",(message.guild.id,))
    gpf = cursor.fetchone()
    if not gpf:
        cursor.execute("INSERT INTO guilds(id,levels,commands,hash,levelupsendto,reward,jltasks,lockcom,sendlog,prefix,lang) VALUES(?,?,?,?,?,?,?,?,?,?,?)", (message.guild.id,{},{},[],None,{},{},[],None,[],None))
        try:
            await message.channel.send(f"{bot.get_emoji(653161518153596950)}このサーバーの思惟奈ちゃんサーバープロファイルを作成しました！いくつかの項目はコマンドを使って書き換えることができます。詳しくはヘルプ(`s-help`)をご覧ください。\n以前からの利用者へ:様々な設定がリセットされています。再設定をお願いします。また、不具合がありましたら`mii-10#3110`にお願いします。")
        except:
            pass
    cursor.execute("select * from guilds where id=?",(message.guild.id,))
    gs = cursor.fetchone()


    tks=[asyncio.ensure_future(dlevel(message,gs)),asyncio.ensure_future(gahash(message,gs)),asyncio.ensure_future(runsercmd(message,gs,pf))]
    await asyncio.gather(*tks)
    tpf=["s-"]+pf["prefix"]+gs["prefix"]
    bot.command_prefix = tpf 
    ctx = await bot.get_context(message)
    try:
        if ctx.command:
            if ctx.command.name in gs["lockcom"] and not ctx.author.guild_permissions.administrator:
                await ctx.send(textto("comlock-locked",ctx.author))
            else:
                await bot.process_commands(message)
    except SystemExit:
        sys.exit()
    except Exception:
        print(traceback.format_exc(0))

async def runsercmd(message,gs,pf):
    #servercmd
    if not "scom" in gs["lockcom"]:
        if not message.author.id == bot.user.id and message.webhook_id is None: 
            tpf=pf["prefix"]+gs["prefix"]
            tpf.append("s-")
            try:
                if not gs["commands"] == None:
                    cmds = gs["commands"]
                    ctts = message.content.split(" ")
                    for k,v in cmds.items():
                        for px in tpf:
                            if px+k == ctts[0]:
                                DoServercmd = True
                                if v["mode"] == "random":
                                    await message.channel.send(random.choice(v["rep"]))
                                elif v["mode"] == "one":
                                    await message.channel.send(v["rep"])
                                elif v["mode"] == "role":
                                    try:
                                        role =message.guild.get_role(v["rep"])
                                    except:
                                        await message.channel.send(textto("scmd-notfound-role",message.author))
                                    if role < message.author.top_role:
                                        if role in message.author.roles:
                                            await message.author.remove_roles(role)
                                            await message.channel.send(textto("scmd-delrole",message.author))
                                        else:
                                            await message.author.add_roles(role)
                                            await message.channel.send(textto("scmd-addrole",message.author))
                                    else:
                                        await message.channel.send(textto("scmd-notrole",message.author))
                                break
            except:
                pass

async def gahash(message,gs):
    if message.channel.id == 611117238464020490:
        if message.embeds:
            cursor.execute("select * from globalchs where name=?",("防災情報",))
            chs = cursor.fetchone()
            es = message.embeds
            sed=[]
            for e in es:
                e.color = ec
                e.title = f'💠{str(e.title).replace("Embed.Empty","防災情報")}'
                sed.append(e)
            for chid in chs["ids"]:
                try:
                    ch = bot.get_channel(chid)
                    for wh in await ch.webhooks():
                        try:
                            if wh.name == "sina_global":
                                await wh.send(embeds=sed)
                                await asyncio.sleep(0.2)
                                break
                        except:
                            continue
                except:
                    pass
    #hash
    if not "hash" in gs["lockcom"]:
        ch=gs["hash"]
        if not ch is []:
            menchan = message.channel_mentions
            for sch in menchan:
                if sch.id in ch:
                    if message.channel.is_nsfw():
                        embed = discord.Embed(title="", description=f"ハッシュタグ投稿\nNSFWチャンネルの投稿につき、コンテンツは隠されています。", color=message.author.color)
                        embed.add_field(name="投稿元チャンネル", value=f"メンション:{message.channel.mention}\n名前:{message.channel.name}")
                        embed.add_field(name="この投稿を見る(see the post)", value=message.jump_url)
                        embed.set_author(name=message.author.display_name, icon_url=message.author.avatar_url_as(static_format='png'))
                    else:
                        embed = discord.Embed(title="", description=message.content, color=message.author.color)
                        embed.add_field(name="投稿元チャンネル", value=f"メンション:{message.channel.mention}\n名前:{message.channel.name}")
                        embed.add_field(name="この投稿を見る(see the post)", value=message.jump_url)
                        embed.set_author(name=message.author.display_name, icon_url=message.author.avatar_url_as(static_format='png'))
                        if not message.attachments == [] and (not message.attachments[0].is_spoiler()):
                            embed.set_image(url=message.attachments[0].url)
                    await sch.send(embed=embed)
    

async def dlevel(message,gs):
    if "clevel" in gs["lockcom"]:
        return
    if message.author.bot:
        return
    if gs["levels"].get(str(message.author.id),None) is None:
        gs["levels"][str(message.author.id)]={
            "level":0,
            "exp":random.randint(5,15),
            "lltime":int(time.time()),
            "dlu":True
        }
        cursor.execute("UPDATE guilds SET levels = ? WHERE id = ?", (gs["levels"],message.guild.id))
    else:
        if gs["levels"][str(message.author.id)]["dlu"]:
            if (int(time.time())-gs["levels"][str(message.author.id)]["lltime"]) >= 60:
                gs["levels"][str(message.author.id)]["lltime"]=int(time.time())
                gs["levels"][str(message.author.id)]["exp"] += random.randint(5,15)
                if gs["levels"][str(message.author.id)]["exp"] >= gs["levels"][str(message.author.id)]["level"] ** 3 + 20:
                    gs["levels"][str(message.author.id)]["exp"] -= gs["levels"][str(message.author.id)]["level"] ** 3 + 20
                    gs["levels"][str(message.author.id)]["level"] += 1
                    aut = str(message.author).replace("\\","\\\\").replace("*","\*").replace("_","\_").replace("|","\|").replace("~","\~").replace("`","\`").replace(">","\>")
                    if gs["levelupsendto"]:
                        c=bot.get_channel(gs["levelupsendto"])
                        try:
                            m = await c.send(str(bot.get_emoji(653161518212448266))+textto("levelup-notify",message.author).format(aut,gs["levels"][str(message.author.id)]["level"]))
                            await asyncio.sleep(1)
                            await m.edit(content=str(bot.get_emoji(653161518212448266))+textto("levelup-notify",message.author).format(message.author.mention,gs["levels"][str(message.author.id)]["level"]))
                        except:
                            pass
                    else:
                        try:
                            m = await message.channel.send(str(bot.get_emoji(653161518212448266))+textto("levelup-notify",message.author).format(aut,gs["levels"][str(message.author.id)]["level"]))
                            await asyncio.sleep(1)
                            await m.edit(content=str(bot.get_emoji(653161518212448266))+textto("levelup-notify",message.author).format(message.author.mention,gs["levels"][str(message.author.id)]["level"]))
                        except:
                            pass
                    if gs["reward"].get(str(gs["levels"][str(message.author.id)]["level"]),None):
                        rl = message.guild.get_role(gs["reward"][str(gs["levels"][str(message.author.id)]["level"])])
                        await message.author.add_roles(rl)
                cursor.execute("UPDATE guilds SET levels = ? WHERE id = ?", (gs["levels"],message.guild.id))

@bot.command()
async def userprefix(ctx,mode="view",ipf=""):
    cursor.execute("select * from users where id=?",(ctx.author.id,))
    upf = cursor.fetchone()
    if mode=="view":
        await ctx.send(embed=getEmbed("ユーザーのprefix",f'```{",".join(upf["prefix"])}```'))
    elif mode=="set":
        spf = upf["prefix"]+[ipf]
        cursor.execute("UPDATE users SET prefix = ? WHERE id = ?", (spf,ctx.author.id))
        await ctx.send(textto("upf-add",ctx.author).format(ipf))
    elif mode=="del":
        spf = upf["prefix"]
        spf.remove(ipf)
        cursor.execute("UPDATE users SET prefix = ? WHERE id = ?", (spf,ctx.author.id))
        await ctx.send(f"prefixから{ipf}を削除しました。")
    else:
        await ctx.send(embed=getEmbed("不適切なモード選択","`view`または`set`または`del`を指定してください。"))

@bot.command()
async def ping(ctx):
    print(f'{ctx.message.author.name}({ctx.message.guild.name})_'+ ctx.message.content )
    startt = time.time()
    mes = await ctx.send("please wait")
    await mes.edit(content=str(round(time.time()-startt,3)*1000)+"ms")

@bot.command()
@commands.is_owner()
async def cu(ctx):
    await ctx.send("see you...")
    await bot.close()

@bot.command(name="level",aliases=["レベルカード", "レベルを見せて"])
@commands.cooldown(1, 20, type=commands.BucketType.user)
async def level(ctx, tu:commands.MemberConverter=None):
    if tu:
        u = tu
    else:
        u =  ctx.author
    LEVEL_FONT = "meiryo.ttc"
    print(f'{ctx.message.author.name}({ctx.message.guild.name})_'+ ctx.message.content )
    if ctx.channel.permissions_for(ctx.guild.me).attach_files == True:
        cursor.execute("select * from guilds where id=?",(ctx.guild.id,))
        gs=cursor.fetchone()
        level=gs["levels"]
        if level.get(str(u.id),None) is None:
            await ctx.send(textto("level-notcount",ctx.author))
        else:
            async with ctx.message.channel.typing():
                nowl = level[str(u.id)]['level']
                exp = level[str(u.id)]['exp']
                nextl = nowl ** 3 + 20
                tonextexp = nextl - exp
                nextl = str(nextl)
                tonextexp = str(tonextexp)
                try:
                    r = requests.get(u.avatar_url_as(static_format="png"), stream=True)
                    if r.status_code == 200:
                        with open("usericon.png", 'wb') as f:
                            f.write(r.content)
                    dlicon = Image.open('usericon.png', 'r')
                except:
                    dlicon = Image.open('noimg.png', 'r')
                dlicon = dlicon.resize((100, 100))
                cursor.execute("select * from users where id=?",(u.id,))
                c = cursor.fetchone()
                cb=c["levcard"] or "m@ji☆"
                cv = Image.open(cb+'.png','r')
                cv.paste(dlicon, (200, 10))
                dt = ImageDraw.Draw(cv)
                fonta = ImageFont.truetype(LEVEL_FONT, 30)
                fontb = ImageFont.truetype(LEVEL_FONT, 42)
                fontc = ImageFont.truetype(LEVEL_FONT, 20)
                if len(u.display_name) > 11:
                    etc = "…"
                else:
                    etc = ""
                if cb=="kazuta123-a" or cb=="kazuta123-b" or cb=="kazuta123-c" or cb=="tomohiro0405":
                    dt.text((300, 60), u.display_name[0:10] +etc, font=fonta, fill='#ffffff')

                    dt.text((50, 110), textto("lc-level",u)+str(level[str(u.id)]['level']) , font=fontb, fill='#ffffff')

                    dt.text((50, 170), textto("lc-exp",u) + str(level[str(u.id)]['exp'])+"/"+nextl , font=fonta, fill='#ffffff')

                    dt.text((50, 210), textto("lc-next",u)+tonextexp , font=fontc, fill='#ffffff')

                    dt.text((50, 300), textto("lc-createdby",u).format(cb.replace("m@ji☆","おあず").replace("kazuta123","kazuta246").replace("-a","").replace("-b","").replace("-c","")) , font=fontc, fill='#ffffff')
                else:
                    dt.text((300, 60), u.display_name[0:10] +etc, font=fonta, fill='#000000')

                    dt.text((50, 110), textto("lc-level",u)+str(level[str(u.id)]['level']) , font=fontb, fill='#000000')

                    dt.text((50, 170), textto("lc-exp",u) + str(level[str(u.id)]['exp'])+"/"+nextl , font=fonta, fill='#000000')

                    dt.text((50, 210), textto("lc-next",u)+tonextexp , font=fontc, fill='#000000')

                    dt.text((50, 300), textto("lc-createdby",u).format(cb.replace("m@ji☆","おあず").replace("kazuta123","kazuta246").replace("-a","").replace("-b","").replace("-c","")) , font=fontc, fill='#000000')

                cv.save("sina'slevelcard.png", 'PNG') 
            await ctx.send(file=discord.File("sina'slevelcard.png"))
    else:
        try:
            await ctx.send(embed=discord.Embed(title=textto("dhaveper",ctx.author),description=textto("per-sendfile",ctx.author)))
        except:
             await ctx.send(f"{textto('dhaveper',ctx.author)}\n{textto('per-sendfile',ctx.author)}")           


@bot.command(name="serverinfo")
async def ginfo(ctx):
    if ctx.guild.id in [i[0] for i in partnerg]:
        ptn="🔗パートナーサーバー:"
    else:
        ptn=""
    page = 0
    e =discord.Embed(title=textto("ginfo-ov-title",ctx.author),color=ec)
    e.set_author(name=f"{ptn}{ctx.guild.name}",icon_url=ctx.guild.icon_url_as(static_format='png'))
    e.add_field(name=textto("ginfo-region",ctx.author),value=ctx.guild.region)
    e.add_field(name=textto("ginfo-afkch",ctx.author),value=ctx.guild.afk_channel)
    if ctx.guild.afk_channel:
        e.add_field(name=textto("ginfo-afktout",ctx.author),value=f"{ctx.guild.afk_timeout/60}min")
    else:
        e.add_field(name=textto("ginfo-afktout",ctx.author),value=textto("ginfo-afknone",ctx.author))
    e.add_field(name=textto("ginfo-sysch",ctx.author),value=ctx.guild.system_channel)
    e.add_field(name=textto("ginfo-memjoinnotif",ctx.author),value=ctx.guild.system_channel_flags.join_notifications)
    e.add_field(name=textto("ginfo-serverboostnotif",ctx.author),value=ctx.guild.system_channel_flags.premium_subscriptions)
    if ctx.guild.default_notifications == discord.NotificationLevel.all_messages:
        e.add_field(name=textto("ginfo-defnotif",ctx.author),value=textto("ginfo-allmsg",ctx.author))
    else:
        e.add_field(name=textto("ginfo-defnotif",ctx.author),value=textto("ginfo-omention",ctx.author))
    if "INVITE_SPLASH" in ctx.guild.features:
        e.add_field(name="招待のスプラッシュ画像",value="下に表示")
        e.set_image(url=ctx.guild.splash_url_as(format="png"))
    if "BANNER" in ctx.guild.features:
        e.add_field(name="サーバーバナー",value="右上に表示")
        e.set_thumbnail(url=ctx.guild.banner_url_as(format="png"))
    mp = await ctx.send(embed=e)
    await mp.add_reaction(bot.get_emoji(653161518195671041))
    await mp.add_reaction(bot.get_emoji(653161518170505216))
    while True:
        try:
            r, u = await bot.wait_for("reaction_add", check=lambda r,u: r.message.id==mp.id and u.id == ctx.message.author.id,timeout=30)
        except:
            break
        try:
            await mp.remove_reaction(r,u)
        except:
            pass
        if str(r) == str(bot.get_emoji(653161518170505216)):
            if page == 11:
                page = 0
            else:
                page = page + 1
        elif str(r) == str(bot.get_emoji(653161518195671041)):
            if page == 0:
                page = 11
            else:
                page = page - 1
        try:
            if page == 0:
                #概要
                e =discord.Embed(title=textto("ginfo-ov-title",ctx.author),color=ec)
                e.set_author(name=f"{ptn}{ctx.guild.name}",icon_url=ctx.guild.icon_url_as(static_format='png'))
                e.add_field(name=textto("ginfo-region",ctx.author),value=ctx.guild.region)
                e.add_field(name=textto("ginfo-afkch",ctx.author),value=ctx.guild.afk_channel)
                if ctx.guild.afk_channel:
                    e.add_field(name=textto("ginfo-afktout",ctx.author),value=f"{ctx.guild.afk_timeout/60}min")
                else:
                    e.add_field(name=textto("ginfo-afktout",ctx.author),value=textto("ginfo-afknone",ctx.author))
                e.add_field(name=textto("ginfo-sysch",ctx.author),value=ctx.guild.system_channel)
                e.add_field(name=textto("ginfo-memjoinnotif",ctx.author),value=ctx.guild.system_channel_flags.join_notifications)
                e.add_field(name=textto("ginfo-serverboostnotif",ctx.author),value=ctx.guild.system_channel_flags.premium_subscriptions)
                if ctx.guild.default_notifications == discord.NotificationLevel.all_messages:
                    e.add_field(name=textto("ginfo-defnotif",ctx.author),value=textto("ginfo-allmsg",ctx.author))
                else:
                    e.add_field(name=textto("ginfo-defnotif",ctx.author),value=textto("ginfo-omention",ctx.author))
                if "INVITE_SPLASH" in ctx.guild.features:
                    e.add_field(name="招待のスプラッシュ画像",value="下に表示")
                    e.set_image(url=ctx.guild.splash_url_as(format="png"))
                if "BANNER" in ctx.guild.features:
                    e.add_field(name="サーバーバナー",value="右上に表示")
                    e.set_thumbnail(url=ctx.guild.banner_url_as(format="png"))
                await mp.edit(embed=e)
            elif page == 1:
                #管理
                e = discord.Embed(title=textto("ginfo-manage",ctx.author),color=ec)
                if ctx.guild.verification_level == discord.VerificationLevel.none:
                    e.add_field(name=textto("ginfo-vlevel",ctx.author),value=textto("ginfo-vlnone",ctx.author))
                elif ctx.guild.verification_level == discord.VerificationLevel.low:
                    e.add_field(name=textto("ginfo-vlevel",ctx.author),value=textto("ginfo-vl1",ctx.author))
                elif ctx.guild.verification_level == discord.VerificationLevel.medium:
                    e.add_field(name=textto("ginfo-vlevel",ctx.author),value=textto("ginfo-vl2",ctx.author))
                elif ctx.guild.verification_level == discord.VerificationLevel.high:
                    e.add_field(name=textto("ginfo-vlevel",ctx.author),value=textto("ginfo-vl3",ctx.author))
                elif ctx.guild.verification_level == discord.VerificationLevel.extreme:
                    e.add_field(name=textto("ginfo-vlevel",ctx.author),value=textto("ginfo-vl4",ctx.author))
                if ctx.guild.explicit_content_filter == discord.ContentFilter.disabled:
                    e.add_field(name=textto("ginfo-filter",ctx.author),value=textto("ginfo-fnone",ctx.author))
                elif ctx.guild.explicit_content_filter == discord.ContentFilter.no_role:
                    e.add_field(name=textto("ginfo-filter",ctx.author),value=textto("ginfo-f1",ctx.author))
                elif ctx.guild.explicit_content_filter == discord.ContentFilter.all_members:
                    e.add_field(name=textto("ginfo-filter",ctx.author),value=textto("ginfo-f2",ctx.author))
                await mp.edit(embed=e)
            elif page == 2:
                #roles
                if ctx.author.guild_permissions.manage_roles or ctx.author.id == 404243934210949120:
                    rl = ctx.guild.roles[::-1]
                    await mp.edit(embed=discord.Embed(title=textto("ginfo-roles",ctx.author),description="\n".join([str(i) for i in rl]),color=ec))
                else:
                    await mp.edit(embed=discord.Embed(title=textto("ginfo-roles",ctx.author),description=textto("ginfo-cantview",ctx.author),color=ec))
            elif page == 3:
                #emoji
                ejs=""
                for i in ctx.guild.emojis:
                    if len( ejs + "," + str(i) ) >=1998:
                        ejs=ejs+"など"
                        break
                    else:
                        ejs=ejs + "," + str(i)
                await mp.edit(embed=discord.Embed(title=textto("ginfo-emoji",ctx.author),description=ejs,color=ec))
            elif page == 4:
                #webhooks
                if ctx.author.guild_permissions.manage_webhooks or ctx.author.id == 404243934210949120:
                    await mp.edit(embed=discord.Embed(title="webhooks",description="\n".join([f"{i.name},[link]({i.url}),created by {i.user}" for i in await ctx.guild.webhooks()]),color=ec))
                else:
                    await mp.edit(embed=discord.Embed(title="webhooks",description=textto("ginfo-cantview",ctx.author),color=ec))
            elif page == 5:
                #ウィジェット
                if ctx.author.guild_permissions.manage_guild or ctx.author.id == 404243934210949120:
                    try:
                        wdt = await ctx.guild.widget()
                        await mp.edit(embed=discord.Embed(title=textto("ginfo-widget",ctx.author),description=f"URL: {wdt.json_url}",color=ec))
                    except:
                        await mp.edit(embed=discord.Embed(title=textto("ginfo-widget",ctx.author),description=textto("ginfo-ctuw",ctx.author),color=ec))
                else:
                    await mp.edit(embed=discord.Embed(title=textto("ginfo-widget",ctx.author),description=textto("ginfo-cantview",ctx.author),color=ec))
            elif page == 6:
                #Nitro server boost
                e = discord.Embed(title=str(bot.get_emoji(653161518971617281))+"Nitro Server Boost",description=f"Level:{ctx.guild.premium_tier}\n({ctx.guild.premium_subscription_count})",color=ec)
                e.add_field(name=textto("ginfo-bst-add",ctx.author),value=textto(f"ginfo-blev{ctx.guild.premium_tier}",ctx.author))
                await mp.edit(embed=e)
            elif page == 7:
                #member
                vml=textto("ginfo-strlenover",ctx.author)
                if len("\n".join([f"{str(i)}" for i in ctx.guild.members])) <= 1024:
                    vml = "\n".join([f"{str(i)}" for i in ctx.guild.members]).replace(str(ctx.guild.owner),f"👑{str(ctx.guild.owner)}")
                await mp.edit(embed=discord.Embed(title="member",description=f"member count:{len(ctx.guild.members)}\n```"+vml+"```"),color=ec)
            elif page == 8:
                if ctx.author.guild_permissions.manage_guild or ctx.author.id == 404243934210949120:
                    try:
                        vi = await ctx.guild.vanity_invite()
                        vi = vi.code
                    except:
                        vi = "NF_VInvite"
                    #invites
                    vil = textto("ginfo-strlenover",ctx.author)
                    if len("\n".join([f"{i.code},利用数:{i.uses}/{i.max_uses},作成者:{i.inviter}" for i in await ctx.guild.invites()])) <= 1023:
                        vil = "\n".join([f"{i.code},利用数:{i.uses}/{i.max_uses},作成者:{i.inviter}" for i in await ctx.guild.invites()]).replace(vi,f"{bot.get_emoji(653161518103265291)}{vi}")
                    await mp.edit(embed=discord.Embed(title=textto("ginfo-invites",ctx.author),description=vil),color=ec)
                else:
                    await mp.edit(embed=discord.Embed(title=textto("ginfo-invites",ctx.author),description=textto("ginfo-cantview",ctx.author),color=ec))
            elif page == 9:
                if ctx.author.guild_permissions.ban_members or ctx.author.id == 404243934210949120:
                    #ban_user 
                    vbl=textto("ginfo-strlenover",ctx.author)
                    bl = []
                    for i in await ctx.guild.bans():
                        bl.append(f"{i.user},reason:{i.reason}")
                    if len("\n".join(bl)) <= 1024:
                        vbl = "\n".join(bl)
                    await mp.edit(embed=discord.Embed(title=textto("ginfo-banneduser",ctx.author),description=vbl),color=ec)
                else:
                    await mp.edit(embed=discord.Embed(title=textto("ginfo-banneduser",ctx.author),description=textto("ginfo-cantview",ctx.author),color=ec))
            elif page == 10:
                #サーバーのチャンネル
                e =discord.Embed(title="チャンネル一覧",color=ec)
                for mct,mch in ctx.guild.by_category():
                    chs="\n".join([i.name for i in mch])
                    e.add_field(name=str(mct).replace("None","カテゴリーなし"),value=f"```{chs}```",inline=True)
                await mp.edit(embed=e)
            elif page == 11:
                cursor.execute("select * from guilds where id=?",(ctx.guild.id,))
                gs = cursor.fetchone()
                e =discord.Embed(title="other",color=ec)
                e.add_field(name="owner",value=ctx.guild.owner.mention)
                e.add_field(name="features",value=f"```{','.join(ctx.guild.features)}```")
                e.add_field(name=textto("ginfo-sinagprofile",ctx.author),value=textto("ginfo-gprodesc",ctx.author).format(gs["reward"],gs["sendlog"],gs["prefix"],gs["lang"],))
                await mp.edit(embed=e)
        except:
            await mp.edit(embed=discord.Embed(title=textto("ginfo-anyerror-title",ctx.author),description=textto("ginfo-anyerror-desc",ctx.author).format(traceback.format_exc(0)),color=ec))


@bot.command(aliases=["グローバルチャットの色を変える"])
async def globalcolor(ctx,color='0x000000'):
    print(f'{ctx.message.author.name}({ctx.message.guild.name})_'+ ctx.message.content )
    cursor.execute("UPDATE users SET gcolor = ? WHERE id = ?", (int(color,16),ctx.author.id))
    await ctx.send(textto("global-color-changed",ctx.message.author))

@bot.command(aliases=["グローバルチャットのニックネームを変える"])
async def globalnick(ctx,nick):
    print(f'{ctx.message.author.name}({ctx.message.guild.name})_'+ ctx.message.content )
    if 1<len(nick)<29:
        cursor.execute("UPDATE users SET gnick = ? WHERE id = ?", (nick,ctx.author.id))
        await ctx.send(textto("global-nick-changed",ctx.message.author))
    else:
        await ctx.send("名前の長さは2文字以上28文字以下にしてください。")


@bot.command(aliases=["グローバルチャットのステータス","グローバルチャットのステータスを見せて"])
async def gprofile(ctx,uid:int=None):
    print(f'{ctx.message.author.name}({ctx.message.guild.name})_'+ ctx.message.content )
    if uid==None:
        cid = ctx.author.id
    else:
        cid = uid
    cursor.execute("select * from users where id=?",(cid,))
    upf = cursor.fetchone()
    embed = discord.Embed(title=textto("global-status-title",ctx.message.author).format(cid), description="", color=upf["gcolor"])
    embed.add_field(name="banned", value=upf["gban"])
    embed.add_field(name="nick", value=upf["gnick"])
    embed.add_field(name="color", value=str(upf["gcolor"]))
    embed.add_field(name="gmod", value=upf["gmod"])
    embed.add_field(name="tester", value=upf["galpha"])
    embed.add_field(name="star", value=upf["gstar"])
    embed.add_field(name="partner", value=upf["sinapartner"])
    await ctx.send(embed=embed)

@bot.command()
async def globalban(ctx,uid:int,ban:bool=True,rea="なし"):
    print(f'{ctx.message.author.name}({ctx.message.guild.name})_'+ ctx.message.content )
    cursor.execute("select * from users where id=?",(ctx.author.id,))
    upf = cursor.fetchone()
    if upf["gmod"] == True:
        cursor.execute("UPDATE users SET gban = ? WHERE id = ?", (int(ban),uid))
        await ctx.send(f"ban状態を{str(ban)}にしました。")

@bot.command()
async def globaltester(ctx,uid,bl:bool=True):
    print(f'{ctx.message.author.name}({ctx.message.guild.name})_'+ ctx.message.content )
    cursor.execute("select * from users where id=?",(ctx.author.id,))
    upf = cursor.fetchone()
    if upf["gmod"] == True:
        cursor.execute("UPDATE users SET galpha = ? WHERE id = ?", (int(bl),uid))
        await ctx.send(f"テスト機能の使用を{str(bl)}にしました。")

@bot.command()
@commands.is_owner()
async def globalmod(ctx,uid,bl:bool=True):
    print(f'{ctx.message.author.name}({ctx.message.guild.name})_'+ ctx.message.content )
    cursor.execute("UPDATE users SET gmod = ? WHERE id = ?", (int(bl),uid))
    await ctx.send(f"グローバルモデレーターを{str(bl)}にしました。")

@bot.command()
@commands.is_owner()
async def globalpartner(ctx,uid,bl:bool=True):
    print(f'{ctx.message.author.name}({ctx.message.guild.name})_'+ ctx.message.content )
    cursor.execute("UPDATE users SET sinapartner = ? WHERE id = ?", (int(bl),uid))
    await ctx.send(f"グローバルパートナーを{str(bl)}にしました。")


@bot.command()
@commands.is_owner()
async def globalstar(ctx,uid,bl:bool=True):
    print(f'{ctx.message.author.name}({ctx.message.guild.name})_'+ ctx.message.content )
    cursor.execute("UPDATE users SET gstar = ? WHERE id = ?", (int(bl),uid))
    await ctx.send(f"スターユーザーを{str(bl)}にしました。")

@bot.command()
async def globalguide(ctx):

    embed = discord.Embed(description=gguide, color=ec)
    await ctx.send(embed=embed)

def ondevicon(mem):
    tmp = ""
    if not str(mem.desktop_status)=="offline":
        tmp = tmp+"💻"
    if not str(mem.mobile_status)=="offline":
        tmp = tmp+"📱"
    if not str(mem.web_status)=="offline":
        tmp = tmp+"🌐"
    return tmp

@bot.command()
@commands.cooldown(1, 20, type=commands.BucketType.guild)
async def gdconnect(ctx):
    if ctx.author.permissions_in(ctx.channel).administrator == True or ctx.author.id == 404243934210949120:
        if ctx.channel.permissions_for(ctx.guild.me).manage_webhooks:
            cursor.execute("select * from globalchs")
            chs = cursor.fetchall()
            if chs !=None:
                for ch in chs:
                    if ctx.channel.id in ch["ids"]:
                        ch["ids"].remove(ctx.channel.id)
                        for wh in await ctx.guild.webhooks():
                            if wh.name == "sina_global":
                                wh.delete()
                        db.execute("UPDATE globalchs SET ids = ? WHERE name = ?", (ch["ids"],ch["name"]))
                        await ctx.send(textto("global-disconnect",ctx.message.author))
                        embed = discord.Embed(title="グローバルチャット切断通知", description=f'{ctx.guild.name}の{ctx.channel.name}が`{ch["name"]}`から切断しました。')
                        for cid in ch["ids"]:
                            channel=bot.get_channel(cid)
                            try:
                                await channel.send(embed=embed)
                            except:
                                pass
                        return
            await ctx.send("ここはどのグローバルチャットにも接続されていません！")
        else:
            await ctx.send("webhooksの管理権限がありません！")
    else:
        await ctx.send("このコマンドを実行するには、このサーバーで管理者権限を持つ必要があります。")

@bot.command()
@commands.cooldown(1, 20, type=commands.BucketType.guild)
async def gconnect(ctx,name:str="main",dnf:bool=True):
    cursor.execute("select * from users where id=?",(ctx.author.id,))
    upf = cursor.fetchone()
    if upf["gban"] == 1:
        await ctx.send("あなたは使用禁止なのでコネクトは使えません。")
        return
    if ctx.author.permissions_in(ctx.channel).administrator == True or ctx.author.id == 404243934210949120:
        if ctx.channel.permissions_for(ctx.guild.me).manage_webhooks:
            cursor.execute("select * from globalchs")
            chs = cursor.fetchall()
            if chs !=None:
                for ch in chs:
                    if ctx.channel.id in ch["ids"]:
                        await ctx.send(f"このチャンネルは既に`{ch['name']}`に接続されています！")
                        return
            cursor.execute("select * from globalchs where name=?",(name,))
            chs=cursor.fetchone()
            if chs is None:
                try:
                    ctg = bot.get_guild(560434525277126656).get_channel(582489567840436231)
                    cch = await ctg.create_text_channel(f'gch-{name}')
                    await cch.create_webhook(name="sina_global",avatar=None)
                    cursor.execute("INSERT INTO globalchs(name,ids) VALUES(?,?)",(name,[ctx.channel.id,cch.id]))
                except:
                    cursor.execute("INSERT INTO globalchs(name,ids) VALUES(?,?)",(name,[ctx.channel.id]))
            else:
                db.execute("UPDATE globalchs SET ids = ? WHERE name = ?", (chs["ids"]+[ctx.channel.id],name))
            await ctx.channel.create_webhook(name="sina_global",avatar=None)
            if dnf:
                embed = discord.Embed(title=f"{bot.get_emoji(653161518174699541)}グローバルチャット接続通知", description=f'{ctx.guild.name}の{ctx.channel.name}が`{name}`に接続しました。')
            else:
                embed = discord.Embed(title="グローバルチャット接続通知", description=f'{bot.get_emoji(653161518174699541)}どこかが`{name}`に接続しました。')
            cursor.execute("select * from globalchs where name=?",(name,))
            ch = cursor.fetchone()
            for cid in ch["ids"]:
                channel=bot.get_channel(cid)
                try:
                    await channel.send(embed=embed)
                except:
                    pass
        else:
            await ctx.send("webhooksの管理権限がありません！")
    else:
        await ctx.send("このコマンドを実行するには、このサーバーで管理者権限を持つ必要があります。")

@bot.command()
@commands.cooldown(1, 30, type=commands.BucketType.user)
async def globaldel(ctx,gmid:int,gchn:str):
    cursor.execute("select * from globalchs where name = ?",(gchn,))
    ch = cursor.fetchone()
    cursor.execute("select * from users where id=?",(ctx.author.id,))
    upf = cursor.fetchone()
    post=None
    cursor.execute("select * from globaldates")
    dats = cursor.fetchall()
    if upf["gmod"]:
        for i in dats:
            if gmid in i["allid"]:
                post = i
        if post:
            for cid in ch["ids"]:
                ch = bot.get_channel(cid)
                for mid in post["allid"]:
                    try:
                        m = await ch.fetch_message(mid)
                        await m.delete()
                    except:
                        pass
        await ctx.send("削除が完了しました。")

@bot.command()
async def viewgban(ctx):
    cursor.execute("select * from users")
    upf = cursor.fetchall()
    if upf["gmod"]:
        async with ctx.message.channel.typing():
            blist = []
            for i in upf:
                if i["gban"] == True:
                    bu = await bot.fetch_user(i["id"])
                    blist.append(f"ユーザー名:{bu},表示名:{i['gnick']},id:{i['id']}")
            embed=discord.Embed(title=f"banされたユーザーの一覧({len(blist)}名)",description="```\n{0}```".format('\n'.join(blist)),color=ec)
        await ctx.send(embed=embed)

@bot.command(aliases=["一定時間削除"])
async def timemsg(ctx,sec:float):
    await asyncio.sleep(sec)
    await ctx.message.delete()

@bot.command()
async def rg(ctx,cou:int,role:commands.RoleConverter=None):

    if role is None:
        role = ctx.guild.default_role
    if cou >= 1:
        ml = [m.mention for m in role.members if not m.bot]
        ogl = []
        gl = []
        tmp = "hoge"
        while len(ml) >= cou:
            for i in range(cou):
                tmp = random.choice(ml)
                ogl.append(tmp)
                ml.remove(tmp)
            gl.append(ogl)
            ogl=[]
            tmp = "hoge"
        gtxt = "\n".join([f"{'と'.join(m)}" for m in gl])
        ng = ",".join(ml)
        await ctx.send(embed=discord.Embed(title=textto("rg-title",ctx.author),description=textto("rg-desc",ctx.author).format(gtxt,ng), color=ec))
    else:
        await ctx.send(textto("rg-block",ctx.author))

@bot.command()
async def anyuserinfo(ctx,*,uid:int=None):
    if uid:
        try:
            u=await bot.fetch_user(uid)
        except discord.NotFound:
            await ctx.send(textto("aui-nf",ctx.author))
        except discord.HTTPException:
            await ctx.send(textto("aui-he",ctx.author))
        except:
            await ctx.send(textto("aui-othere",ctx.author).format(traceback.format_exc()))
        else:
            if u.id in [i[1] for i in partnerg]:
                ptn=":🔗パートナーサーバーオーナー"
            else:
                ptn=""
            e = discord.Embed(title=f"{textto('aui-uinfo',ctx.author)}{ptn}",color=ec)
            e.add_field(name=textto("aui-name",ctx.author),value=u.name)
            e.add_field(name=textto("aui-id",ctx.author),value=u.id)
            e.add_field(name=textto("aui-dr",ctx.author),value=u.discriminator)
            e.add_field(name=textto("aui-isbot",ctx.author),value=u.bot)
            e.set_thumbnail(url=u.avatar_url)
            e.set_footer(text=textto("aui-created",ctx.author).format(u.created_at))
            e.timestamp = u.created_at
        await ctx.send(embed=e)
    else:
        await ctx.send(textto("aui-nid",ctx.author))

@bot.command()
@commands.cooldown(2, 10, type=commands.BucketType.user)
async def wid(ctx,inid):
    if not textto("language",ctx.author) == "ja":
        await ctx.send(textto("cannot-run",ctx.author))
        return

    async with ctx.message.channel.typing():
        st = time.time()
        try:
            id = int(inid)
        except:
            id = None
        idis = bot.get_channel(id)
        if idis:
            if isinstance(idis,discord.DMChannel):
                await ctx.send(embed=getEmbed("DMチャンネル",f"相手:{idis.recipient}"))
            elif isinstance(idis,discord.GroupChannel):
                await ctx.send(embed=getEmbed("グループDMチャンネル",f"メンバー:{','.join(idis.recipients)},\n名前:{idis.name},"))
            elif isinstance(idis,discord.abc.GuildChannel):
                await ctx.send(embed=getEmbed("サーバーチャンネル",f"名前:{idis.name}\nサーバー:{idis.guild}"))
            else:
                await ctx.send(embed=getEmbed("その他チャンネル"))
            return
        idis = bot.get_guild(id)
        if idis:
            if idis.id in [i[0] for i in partnerg]:
                ptn="🔗パートナーサーバー"
            else:
                ptn=""
            await ctx.send(embed=getEmbed("サーバー",f"{ptn}\n名前:{idis.name}\nid:{idis.id}"))
            return
        try:
            idis = await bot.fetch_user(id)
            u=idis
            e = discord.Embed(title="ユーザー",color=ec)
            e.add_field(name="名前",value=u.name)
            e.add_field(name="id",value=u.id)
            e.add_field(name="ディスクリミネータ",value=u.discriminator)
            e.add_field(name="botかどうか",value=u.bot)
            e.set_thumbnail(url=u.avatar_url)
            e.set_footer(text=f"アカウント作成日時(そのままの値:{u.created_at},タイムスタンプ化:")
            e.timestamp = u.created_at
            await ctx.send(embed=e)
            return
        except:
            pass
        idis = bot.get_emoji(id)
        if idis:
            await ctx.send(embed=getEmbed("絵文字",f"名前:{str(idis)}\nid:{idis.id}"))
            return
        try:
            idis = await bot.fetch_invite(inid)
            await ctx.send(embed=getEmbed("サーバー招待",f"名前:{str(idis.guild.name)}\nチャンネル:{idis.channel.name}\nmember_count:{idis.approximate_member_count}\npresence_count:{idis.approximate_presence_count}\n[参加]({idis.url})"))
            return
        except:
            pass
        try:
            idis = await bot.fetch_webhook(id)
            await ctx.send(embed=getEmbed("webhook",f"デフォルトネーム:{idis.name}\nサーバーid:{idis.guild_id}"))
            return
        except:
            pass
        try:
            idis = await bot.fetch_widget(inid)
            await ctx.send(embed=getEmbed("サーバーウィジェット",f"名前:{idis.name}\n招待:{idis.invite_url}"))
            return
        except:
            pass
        try:
            for g in bot.guilds:
                for ch in g.text_channels:
                    try:
                        idis = await ch.fetch_message(id)
                        await ctx.send(embed=getEmbed("メッセージ",f"送信者:{idis.author}\n内容:{idis.content}"))
                        return
                    except:
                        pass
                    finally:
                        await asyncio.sleep(0.5)
        except:
            pass
        await ctx.send(embed=getEmbed("そのidでは見つかりませんでした。",""))

async def wait_message_return(ctx,stext,sto,tout=60):
    await sto.send(stext)
    return await bot.wait_for('message', check=lambda m: m.author==ctx.author and m.channel==sto,timeout=tout)

@bot.command(name="textlocker")
async def textlocker(ctx):
    if not textto("language",ctx.author) == "ja":
        await ctx.send(textto("cannot-run",ctx.author))
        return

    dc = await opendm(ctx.author)
    askmd=await dc.send(embed=getEmbed("テキスト暗号・複合","暗号化する場合は🔒を、復号する場合は🔓を押してください。"))
    await askmd.add_reaction('🔒')
    await askmd.add_reaction('🔓')
    try:
        r,u= await bot.wait_for("reaction_add", check=lambda r,u: str(r.emoji) in ["🔒","🔓"] and r.message.id==askmd.id and u.bot==False,timeout=60)
    except asyncio.TimeoutError:
        await ctx.send("タイムアウトしました。初めからやり直してください。")
        return
    if str(r.emoji) == "🔒":
        setting={}
        rtxt = await wait_message_return(ctx,"暗号化する文を送ってください。",dc)
        setting["text"] = rtxt.content.lower()
        rtxt = await wait_message_return(ctx,"始めのずらしを送ってください。",dc)
        setting["zs"] = int(rtxt.content)
        rtxt = await wait_message_return(ctx,"パターンを変えるまでの数を送ってください。",dc)
        setting["cp"] = int(rtxt.content)
        rtxt = await wait_message_return(ctx,"変えるときのずらす数を送ってください。",dc)
        setting["cpt"] = int(rtxt.content)
        rtext = ""
        tcount = 0
        zcount = 0
        uzs = setting["zs"]
        while tcount <= len(setting["text"])-1:
            zcount = zcount + 1
            ztmp = tl.find(setting["text"][tcount])
            if not ztmp == -1:
                if ztmp+uzs >= len(tl):
                    rtext = f"{rtext}{tl[ztmp+uzs-len(tl)]}"
                else:
                    rtext = f"{rtext}{tl[ztmp+uzs]}"
                if zcount == setting["cp"]:
                    uzs = uzs + setting["cpt"]
                    zcount = 0
            else:
                rtext = f"{rtext}☒"
            tcount = tcount + 1
        await dc.send(f"`{rtext}`になりました。")
    elif str(r.emoji) == "🔓":
        setting={}
        rtxt = await wait_message_return(ctx,"復号する文を送ってください。",dc)
        setting["text"] = rtxt.content
        rtxt = await wait_message_return(ctx,"始めのずらしを送ってください。",dc)
        setting["zs"] = int(rtxt.content)
        rtxt = await wait_message_return(ctx,"パターンを変えるまでの数を送ってください。",dc)
        setting["cp"] = int(rtxt.content)
        rtxt = await wait_message_return(ctx,"変えるときのずらす数を送ってください。",dc)
        setting["cpt"] = int(rtxt.content)
        rtext = ""
        tcount = 0
        zcount = 0
        uzs = setting["zs"]
        while tcount <= len(setting["text"])-1:
            zcount = zcount + 1
            ztmp = tl.find(setting["text"][tcount])
            if not ztmp == -1:
                if ztmp+uzs < 0:
                    rtext = f"{rtext}{tl[ztmp-uzs+len(tl)]}"
                else:
                    rtext = f"{rtext}{tl[ztmp-uzs]}"
                if zcount == setting["cp"]:
                    uzs = uzs + setting["cpt"]
                    zcount = 0
            else:
                rtext = f"{rtext}☒"
            tcount = tcount + 1
        await dc.send(f"`{rtext}`になりました。")
    else:
        await ctx.send("絵文字が違います。")

@bot.command()
async def roletrans(ctx,gid:int):
    try:
        g = bot.get_guild(gid)
        if ctx.author.permissions_in(ctx.channel).administrator == True or ctx.author.id == 404243934210949120:
            async with ctx.channel.typing():
                for r in g.roles[1:][::-1]:
                    await ctx.guild.create_role(name=r.name,permissions=r.permissions,colour=r.colour,hoist=r.hoist,mentionable=r.mentionable,reason=f"{g.name}より。役職転送コマンド実行による。")
                    await asyncio.sleep(2)
            await ctx.send("完了しました。")
        else:
            await ctx.send("このサーバーの管理者である必要があります。")
    except:
        await ctx.send(embed=getEmbed("エラー",f"詳細:```{traceback.format_exc(0)}```"))

@bot.command()
async def chtrans(ctx,gid:int):
    try:
        g = bot.get_guild(gid)
        if ctx.author.permissions_in(ctx.channel).administrator == True or ctx.author.id == 404243934210949120:
            async with ctx.channel.typing():
                #すること
                for mct,mch in g.by_category():
                    await asyncio.sleep(2)
                    try:
                        ct = await ctx.guild.create_category_channel(name=mct.name)
                    except AttributeError:
                        ct = None
                    for c in mch:
                        await asyncio.sleep(2)
                        if isinstance(c,discord.TextChannel):
                            await ctx.guild.create_text_channel(name=c.name,category=ct,topic=c.topic,slowmode_delay=c.slowmode_delay,nsfw=c.is_nsfw())
                        elif isinstance(c,discord.VoiceChannel):
                            await ctx.guild.create_voice_channel(name=c.name,category=ct,bitrate=c.bitrate,user_limit=c.user_limit)
                        else:
                            pass            
            await ctx.send("完了しました。")
        else:
            await ctx.send(textto("need-admin",ctx.author))
    except:
        await ctx.send(embed=getEmbed(textto("ginfo-anyerror-title",ctx.author),textto("ginfo-anyerror-title",ctx.author).format(traceback.format_exc(0))))

@bot.command()
async def levelupsendto(ctx,to):
    if to == "here":
        cursor.execute("UPDATE guilds SET levelupsendto = ? WHERE id = ?", ("here",ctx.guild.id))
    else:
        cursor.execute("UPDATE guilds SET levelupsendto = ? WHERE id = ?", (int(to),ctx.guild.id))
    await ctx.send(textto("changed",ctx.author))

@bot.command()
async def levelreward(ctx,lv:int,rl:commands.RoleConverter=None):
    rid = rl.id
    if not(ctx.author.permissions_in(ctx.channel).manage_guild == True and ctx.author.permissions_in(ctx.channel).manage_roles == True or ctx.author.id == 404243934210949120):
        await ctx.send(textto("need-admin",ctx.author))
        return
    cursor.execute("select * from guilds where id=?",(ctx.guild.id,))
    gs = cursor.fetchone()
    if rid is None:
        del gs["reward"][str(lv)]
    else:
        gs["reward"][str(lv)] = rid
    cursor.execute("UPDATE guilds SET reward = ? WHERE id = ?", (gs["reward"],ctx.guild.id))
    await ctx.send(textto("changed",ctx.author))

@bot.command()
async def memo(ctx,mode="a",mn="def",ctt=None):
    print(f'{ctx.message.author.name}({ctx.message.guild.name})_'+ ctx.message.content )
    cursor.execute("select * from users where id=?",(ctx.author.id,))
    mmj = cursor.fetchone()
    if mode == "r":
        if not mmj["memo"] == None:
            if mmj["memo"].get(mn) == None:
                await ctx.send(textto("memo-r-notfound1",ctx.message.author))
            else:
                await ctx.send(mmj["memo"][mn])
        else:
            await ctx.send(textto("memo-r-notfound2",ctx.message.author))
    elif mode == "w":
        if ctt == None:
            mmj["memo"][mn] = None
        else:
            mmj["memo"][mn] = ctx.message.content.replace(f's-memo {mode} {mn} ',"")
        cursor.execute("UPDATE users SET memo = ? WHERE id = ?", (mmj["memo"],ctx.author.id))

        await ctx.send(textto("memo-w-write",ctx.message.author).format(str(mn)))
    elif mode == "a":
        if mmj["memo"] == {}:
            await ctx.send(textto("memo-a-notfound",ctx.message.author))
        else:
            await ctx.send(str(mmj["memo"].keys()).replace("dict_keys(",textto("memo-a-list",ctx.message.author)).replace(")",""))
    else:
        await ctx.send(textto("memo-except",ctx.message.author))

@bot.command(name="fish")
@commands.cooldown(1, 5, type=commands.BucketType.user)
async def fishany(ctx):

    lt=["🦑","🦐","🐙","🦀","🐡","🐠","🐟"] + [i.id for i in ctx.guild.emojis]
    fs = random.choice(lt)
    if str(type(fs)) == "<class 'int'>":
        fs = str(bot.get_emoji(fs))
    gp = random.randint(1,3)
    cursor.execute("select * from users where id=?",(ctx.author.id,))
    upf = cursor.fetchone()
    cursor.execute("UPDATE users SET gpoint = ? WHERE id = ?", (gp,ctx.author.id))
    await ctx.send(embed=getEmbed("fish",textto("fish-get",ctx.author).format(fs,gp)))

@bot.command(aliases=["オンライン通知"])
async def onlinenotif(ctx,mode,uid:int):
    cursor.execute("select * from users where id=?",(ctx.author.id,))
    upf = cursor.fetchone()
    if mode=='add':
        upf["onnotif"].append(uid)
        db.execute("UPDATE users SET onnotif = ? WHERE id = ?", (upf["onnotif"],ctx.author.id))
        await ctx.send(textto("onnotif-set",ctx.message.author))
    elif mode =='del':
        upf["onnotif"].remove(uid)
        db.execute("UPDATE users SET onnotif = ? WHERE id = ?", (upf["onnotif"],ctx.author.id))
        await ctx.send(textto("onnotif-stop",ctx.message.author))
    else:
        await ctx.send(textto("onnotif-error",ctx.message.author))
    cursor.execute("select * from users where id=?",(ctx.author.id,))
    upf = cursor.fetchone()
    await ctx.send(f"upf:{upf['onnotif']}")

@bot.command()
async def hash(ctx):
    cursor.execute("select * from guilds where id=?",(ctx.guild.id,))
    d = cursor.fetchone()
    hc = d["hash"]
    if hc == None:
        d["hash"]=[ctx.channel.id]
        await ctx.send(textto("hash-connect",ctx.message.author))
    elif ctx.channel.id in hc:
        d["hash"].remove(ctx.channel.id)
        await ctx.send(textto("hash-disconnect",ctx.message.author))
    else:
        d["hash"].append(ctx.channel.id)
        await ctx.send(textto("hash-connect",ctx.message.author))
    cursor.execute("UPDATE guilds SET hash = ? WHERE id = ?", (d["hash"],ctx.guild.id))

@bot.command(aliases=["サーバーコマンド","次の条件でサーバーコマンドを開く"])
async def servercmd(ctx,mode="all",name=None):
    cursor.execute("select * from guilds where id=?",(ctx.guild.id,))
    mmj = cursor.fetchone()
    print(f'{ctx.message.author.name}({ctx.message.guild.name})_'+ ctx.message.content )
    if mode == "add":
            if not mmj["commands"].get(name,None) is None:
                 if not(ctx.author.permissions_in(ctx.channel).manage_guild == True and ctx.author.permissions_in(ctx.channel).manage_roles == True or ctx.author.id == 404243934210949120):
                     await ctx.send(textto("need-manage",ctx.author))
                     return
            dc = ctx.author.dm_channel
            if dc == None:
                await ctx.author.create_dm()
                dc = ctx.author.dm_channel
            
            emojis = ctx.guild.emojis

            se = [] 
            for e in emojis:
                se = se + [str(e)]
            
            await dc.send(textto("scmd-add-guide1",ctx.message.author))
            
            def check(m):
                return m.channel == dc and m.author == ctx.author

            msg = await bot.wait_for('message', check=check)
            if msg.content =="one":
                await dc.send(textto("scmd-add-guide2",ctx.message.author))
                mes = await bot.wait_for('message', check=check)
                guide=mes.content
                try:
                    await dc.send(textto("scmd-add-guide3-a",ctx.message.author).format(textto("scmd-guide-emoji",ctx.message.author),str(se)))
                except:
                    await dc.send(textto("scmd-add-guide3-a",ctx.message.author).format(textto("scmd-guide-emoji",ctx.message.author),"(絵文字が多すぎて表示できません！)"))
                mg=await bot.wait_for('message', check=check)
                rep = mg.clean_content.format(se)
                mmj["commands"][name]={}
                mmj["commands"][name]["mode"]="one"
                mmj["commands"][name]["rep"]=rep
                mmj["commands"][name]["createdBy"]=ctx.author.name
                mmj["commands"][name]["guide"]=guide
            elif msg.content == "random":
                await dc.send(textto("scmd-add-guide2",ctx.message.author))
                mes = await bot.wait_for('message', check=check)
                guide=mes.content
                try:
                    await dc.send(textto("scmd-add-guide3-a",ctx.message.author).format(textto("scmd-guide-emoji",ctx.message.author),str(se)))
                except:
                    await dc.send(textto("scmd-add-guide3-a",ctx.message.author).format(textto("scmd-guide-emoji",ctx.message.author),"(絵文字が多すぎて表示できません！)"))
                rep = []
                while True:
                    mg=await bot.wait_for('message', check=check)
                    if mg.content=="stop":
                        break
                    else:
                        rep = rep + [mg.clean_content.format(se)]
                        try:
                            await dc.send(textto("scmd-add-guide3-b",ctx.message.author).format(textto("scmd-guide-emoji",ctx.message.author),str(se)))
                        except:
                            await dc.send(textto("scmd-add-guide3-b",ctx.message.author).format(textto("scmd-guide-emoji",ctx.message.author),"(絵文字が多すぎて表示できません！)"))
                mmj["commands"][name]={}
                mmj["commands"][name]["mode"]="random"
                mmj["commands"][name]["rep"]=rep
                mmj["commands"][name]["createdBy"]=ctx.author.name
                mmj["commands"][name]["guide"]=guide
            elif msg.content == "role":
                if ctx.author.permissions_in(ctx.channel).manage_guild == True and ctx.author.permissions_in(ctx.channel).manage_roles == True or ctx.author.id == 404243934210949120:
                    await dc.send(textto("scmd-add-guide2",ctx.message.author))
                    mes = await bot.wait_for('message', check=check)
                    guide=mes.content
                    await dc.send(textto("scmd-add-guide3-c",ctx.message.author).format(textto("scmd-guide-emoji",ctx.message.author),str(se)))
                    mg=await bot.wait_for('message', check=check)
                    rep = int(mg.clean_content)
                    mmj["commands"][name]={}
                    mmj["commands"][name]["mode"]="role"
                    mmj["commands"][name]["rep"]=rep
                    mmj["commands"][name]["createdBy"]=ctx.author.name
                    mmj["commands"][name]["guide"]=guide
                else:
                    await ctx.send(textto("need-manage",ctx.author))
                    return
            else:
                await dc.send(textto("scmd-add-not",ctx.message.author))
                return
            cursor.execute("UPDATE guilds SET commands = ? WHERE id = ?", (mmj["commands"],ctx.guild.id))
            await ctx.send(textto("scmd-add-fin",ctx.message.author))
    elif mode == "help":
        if mmj["commands"] == {}:
            await ctx.send(textto("scmd-all-notfound",ctx.message.author))
        elif mmj["commands"].get(name) is None:
            await ctx.send(textto("scmd-help-notfound",ctx.message.author))
        else:
            await ctx.send(textto("scmd-help-title",ctx.message.author).format(name,mmj["commands"][name]['createdBy'],mmj["commands"][name]['guide']))
    elif mode == "all":
        if mmj["commands"] == []:
            await ctx.send(textto("scmd-all-notfound",ctx.message.author))
        else:
            await ctx.send(str(mmj["commands"].keys()).replace("dict_keys(",textto("scmd-all-list",ctx.message.author)).replace(")",""))
    elif mode == "del":
        if ctx.author.permissions_in(ctx.channel).manage_guild == True and ctx.author.permissions_in(ctx.channel).manage_roles == True or ctx.author.id == 404243934210949120:
            if not mmj["commands"] == None:
                del mmj["commands"][name]
            await ctx.send(textto("scmd-del",ctx.message.author))
            cursor.execute("UPDATE guilds SET commands = ? WHERE id = ?", (mmj["commands"],ctx.guild.id))
        else:
            await ctx.send(textto("need-manage",ctx.author))
    else:
        await ctx.send(textto("scmd-except",ctx.message.author))

@bot.command()
async def setsysmsg(ctx,mode="check",when="welcome",to="sysch",content=None):
    cursor.execute("select * from guilds where id=?",(ctx.guild.id,))
    msgs = cursor.fetchone()
    sm = msgs["jltasks"]
    if mode == "check":
        embed = discord.Embed(title=textto("ssm-sendcontent",ctx.message.author), description=ctx.guild.name, color=ec)
        try:
            embed.add_field(name=textto("ssm-welcome",ctx.message.author), value=f'{sm["welcome"].get("content")}({textto("ssm-sendto",ctx.message.author)}):{sm["welcome"].get("sendto")})')
        except:
            pass
        try:
            embed.add_field(name=textto("ssm-seeyou",ctx.message.author), value=f'{sm["cu"].get("content")}({textto("ssm-sendto",ctx.message.author)}:{sm["cu"].get("sendto")})')
        except:
            pass
        await ctx.send(embed=embed)
    elif mode == "set":
        if ctx.author.permissions_in(ctx.channel).administrator == True or ctx.author.id == 404243934210949120:
            try:
                msgs["jltasks"][when]={}
                msgs["jltasks"][when]["content"] = content
                msgs["jltasks"][when]["sendto"] = to
                cursor.execute("UPDATE guilds SET jltasks = ? WHERE id = ?", (msgs["jltasks"],ctx.guild.id))
                await ctx.send(textto("ssm-set",ctx.message.author))
            except:
                await ctx.send(textto("ssm-not",ctx.message.author))
        else:
            await ctx.send(textto("need-admin",ctx.author))

@bot.command(name="randomint",liases=["randint", "乱数","次の条件で乱数を作って"])
async def randomint(ctx,*args):

    print(f'{ctx.message.author.name}({ctx.message.guild.name})_'+ ctx.message.content )
    if len(args)==1:
        s=1
        e=6
        c=int(args[0])
    elif len(args)==2:
        s=int(args[0])
        e=int(args[1])
        c=1
    elif len(args)==3:
        s=int(args[0])
        e=int(args[1])
        c=int(args[2])
    else:
        await ctx.send(textto("randomint-arg-error",ctx.message.author))
    #try:
    intcount = []
    rnd = 0
    for i in range(c):
        if s <= e:
            tmp =  random.randint(s, e)
            intcount = intcount + [tmp]
            rnd= rnd + tmp
        else:
            tmp =  random.randint(e, s)
            intcount = intcount + [tmp]
            rnd= rnd + tmp
    await ctx.send(textto("randomint-return1",ctx.message.author).format(str(s),str(e),str(c),str(rnd),str(intcount)))
    #except:
        #await ctx.send(textto("randomint-return2",ctx.message.author))

@bot.command(name="fortune",aliases=["おみくじ", "今日のおみくじをひく"])
async def fortune(ctx):

    print(f'{ctx.message.author.name}({ctx.message.guild.name})_'+ ctx.message.content )
    rnd = random.randint(0, 6)
    await ctx.send(textto("omikuzi-return",ctx.message.author).format(textto("omikuzi-"+str(rnd),ctx.message.author)))

@bot.command(name="scranotif",aliases=["snotify", "Scratchの通知","Scratchの通知を調べて"])
@commands.cooldown(1, 5, type=commands.BucketType.user)
async def scranotif(ctx, un:str):

    print(f'{ctx.message.author.name}({ctx.message.guild.name})_'+ ctx.message.content )
    try:
        async with ctx.message.channel.typing():
            url = 'https://api.scratch.mit.edu/users/'+un+'/messages/count'
            response = urllib.request.urlopen(url)
            content = json.loads(response.read().decode('utf8'))
            await ctx.send(textto("scranotif-notify",ctx.message.author).format(un,str(content['count'])))
    except:
        await ctx.send(textto("scranotif-badrequest",ctx.message.author))

@bot.command(aliases=["scratchwikiのurl", "次のページのScratchwikiのURL教えて"])
async def jscrawiki(ctx, un:str):

    print(f'{ctx.message.author.name}({ctx.message.guild.name})_'+ ctx.message.content )
    await ctx.send(textto("jscrawiki-return",ctx.message.author).format(un))

@bot.command(aliases=["scratchのユーザーurl", "次のScratchユーザーのURL教えて"])
async def scrauser(ctx, un:str):

    print(f'{ctx.message.author.name}({ctx.message.guild.name})_'+ ctx.message.content )
    await ctx.send(textto("scrauser-return",ctx.message.author).format(un))
    
@bot.command(aliases=["次の言葉でyoutube調べて"])
@commands.cooldown(1, 10, type=commands.BucketType.user)
async def youtube(ctx):

    print(f'{ctx.message.author.name}({ctx.message.guild.name})_'+ ctx.message.content )
    try:
        async with ctx.message.channel.typing():
            wd = ctx.message.content.replace("s-youtube ", "")
            youtube = build('youtube', 'v3', developerKey=GAPI_TOKEN)
            search_response = youtube.search().list(
            part='snippet',
            q=wd,
            type='video'
            ).execute()
            id = search_response['items'][0]['id']['videoId']
            await ctx.send(textto("youtube-found",ctx.message.author).format(id))        
    except:
        await ctx.send(textto("youtube-notfound",ctx.message.author))  

@bot.command(aliases=["wikipedia","次の言葉でwikipedia調べて"])
@commands.cooldown(1, 10, type=commands.BucketType.user)
async def jwp(ctx):

    try:
        async with ctx.message.channel.typing():
            wd = ctx.message.content.replace("s-jwp ", "")  
            sw = wikipedia.search(wd, results=1)
            sw1 = sw[0].replace(" ", "_")
            sr = wikipedia.page(sw1)
            embed = discord.Embed(title=sw1, description=sr.summary, color=ec)
            embed.add_field(name=textto("jwp-seemore",ctx.message.author), value=f"https://ja.wikipedia.org/wiki/{sw1}")
            try:
                embed.set_image(url=sr.images[0])
            except:
                pass
        await ctx.send(embed=embed)
    except:
        try:
            async with ctx.message.channel.typing():
                if not sw == None:
                    await ctx.send(textto("jwp-found",ctx.message.author).format(wd,sw1))
        except:
            await ctx.send(textto("jwp-notfound",ctx.message.author))

@bot.command(aliases=["天気","今日の天気は"])
@commands.cooldown(1, 15, type=commands.BucketType.user)
async def jpwt(ctx):

    print(f'{ctx.message.author.name}({ctx.message.guild.name})_'+ ctx.message.content )
    if ctx.channel.permissions_for(ctx.guild.me).attach_files == True:
        try:
            async with ctx.message.channel.typing():
                r = requests.get("http://www.jma.go.jp/jp/yoho/images/000_telop_today.png", stream=True)
                if r.status_code == 200:
                    with open("weather.png", 'wb') as f:
                        f.write(r.content)
                    await ctx.send(file=discord.File("weather.png"))
                    await ctx.send(textto("jpwt-credit",ctx.message.author))
        except:
            await ctx.send(textto("jpwt-error",ctx.message.author))
    else:
        try:
            await ctx.send(embed=discord.Embed(title=textto("dhaveper",ctx.message.author),description=textto("per-sendfile",ctx.message.author)))
        except:
                await ctx.send(f"{textto('dhaveper',ctx.message.author)}\n{textto('per-sendfile',ctx.message.author)}")           


@bot.command(aliases=["ニュース","ニュースを見せて"])
@commands.cooldown(1, 15, type=commands.BucketType.user)
async def news(ctx):

    print(f'{ctx.message.author.name}({ctx.message.guild.name})_'+ ctx.message.content )
    content = requests.get('https://newsapi.org/v2/top-headlines?country=jp&pagesize=5&apiKey='+NAPI_TOKEN).json()
    for i in range(int(content["totalResults"]) - 1):
        await ctx.send(content['articles'][i]["url"])

@bot.command(aliases=["switchlevelup"])
async def switchLevelup(ctx):

    print(f'{ctx.message.author.name}({ctx.message.guild.name})_'+ ctx.message.content )
    cursor.execute("select * from guilds where id=?",(ctx.guild.id,))
    dor = cursor.fetchone()
    if dor["levels"][str(ctx.author.id)]["dlu"]:
        dor["levels"][str(ctx.author.id)]["dlu"] = False
        await ctx.send(textto("sLu-off",ctx.message.author))
    else:
        dor["levels"][str(ctx.author.id)]["dlu"] = True
        await ctx.send(textto("sLu-on",ctx.message.author))
    cursor.execute("UPDATE guilds SET levels = ? WHERE id = ?", (dor["levels"],ctx.guild.id))

@bot.command()
@commands.cooldown(1, 5, type=commands.BucketType.user)
async def gwd(ctx):

    print(f'{ctx.message.author.name}({ctx.message.guild.name})_'+ ctx.message.content )
    try:
        async with ctx.message.channel.typing():
            str1 = ctx.message.content.replace("s-gwd ", "")
            sid = requests.get("https://www.wikidata.org/w/api.php?action=wbsearchentities&search="+str1+"&language=en&format=json").json()["search"][0]["id"]
            purl = requests.get("https://www.wikidata.org/w/api.php?action=wbsearchentities&search="+str1+"&language=en&format=json").json()["search"][0]["concepturi"]
            sret = mwc.get(sid, load=True).attributes["claims"]["P569"][0]["mainsnak"]["datavalue"]["value"]["time"]
            vsd = sret.replace("+","")
            vsd = vsd.replace("-","/")
            vsd = vsd.replace("T00:00:00Z","")
        await ctx.send(textto("gwd-return1",ctx.message.author).format(str1,vsd,purl))
    except:
        await ctx.send(textto("gwd-return2",ctx.message.author))

@bot.command()
@commands.cooldown(1, 80)
async def gupd(ctx):

    print(f'{ctx.message.author.name}({ctx.message.guild.name})_'+ ctx.message.content )
    content = requests.get('https://ja.scratch-wiki.info/w/api.php?action=query&list=recentchanges&rcprop=title|timestamp|user|comment|flags|sizes&format=json').json()
    await ctx.send(textto("gupd-send",ctx.message.author))
    for i in range(5):
        try:
            embed = discord.Embed(title=textto("gupd-page",ctx.message.author), description=content["query"]['recentchanges'][i]["title"], color=ec)
            embed.add_field(name=textto("gupd-editor",ctx.message.author), value=content["query"]['recentchanges'][i]["user"])
            embed.add_field(name=textto("gupd-size",ctx.message.author), value=str(content["query"]['recentchanges'][i]["oldlen"])+"→"+str(content["query"]['recentchanges'][i]["newlen"])+"("+str(content["query"]['recentchanges'][i]["newlen"]-content["query"]['recentchanges'][i]["oldlen"])+")")
            embed.add_field(name=textto("gupd-type",ctx.message.author), value=content["query"]['recentchanges'][i]["type"])
            if not content["query"]['recentchanges'][i]["comment"] == "":
                embed.add_field(name=textto("gupd-comment",ctx.message.author), value=content["query"]['recentchanges'][i]["comment"])
            else:
                embed.add_field(name=textto("gupd-comment",ctx.message.author), value=textto("gupd-notcomment",ctx.message.author))
            embed.add_field(name=textto("gupd-time",ctx.message.author), value=content["query"]['recentchanges'][i]["timestamp"].replace("T"," ").replace("Z","").replace("-","/"))
            await ctx.send(embed=embed)
        except:
            eembed = discord.Embed(title=textto("gupd-unknown",ctx.message.author), description=textto("gupd-url",ctx.message.author), color=ec)
            await ctx.send(embed=eembed)

@bot.command(name="near21")
async def game1(ctx,user2:commands.MemberConverter=None):

    print(f'{ctx.message.author.name}({ctx.message.guild.name})_'+ ctx.message.content)
    if ctx.channel.permissions_for(ctx.guild.me).manage_messages == True:
        if user2 == None:
            embed = discord.Embed(title="game1", description=textto("game1-dis",ctx.message.author), color=ec)
            embed.add_field(name=textto("game1-guide1",ctx.message.author), value=textto("game1-guide2",ctx.message.author))
            embed.add_field(name=textto("game1-now",ctx.message.author), value="0")
            guide = await ctx.send(embed=embed)
            g1=await guide.add_reaction(bot.get_emoji(653161517927366658))
            g2=await guide.add_reaction(bot.get_emoji(653161518334214144))
            uint = 0
            tmint= 0
            while(True):

                reaction, user = await bot.wait_for("reaction_add", check=lambda r,u: str(r.emoji) in [str(bot.get_emoji(653161517927366658)),str(bot.get_emoji(653161518334214144))] and r.message.id==guide.id and u == ctx.message.author)

                await guide.remove_reaction(reaction,user)
                if str(reaction.emoji) == str(bot.get_emoji(653161517927366658)):
                    dr = random.randint(1,11)
                    uint = uint + dr
                    embed = discord.Embed(title="game1", description=textto("game1-dis",ctx.message.author), color=ec)
                    embed.add_field(name=textto("game1-guide1",ctx.message.author), value=textto("game1-guide2",ctx.message.author), inline=False)
                    embed.add_field(name=textto("game1-now",ctx.message.author), value=str(uint)+"(+"+str(dr)+")")
                    if tmint < random.randint(10,21):
                        tmdr = random.randint(1,11)
                        tmint = tmint + tmdr
                        embed.add_field(name=textto("game1-cpun",ctx.message.author), value=textto("game1-cpud",ctx.message.author))
                    else:
                        embed.add_field(name=textto("game1-cpun",ctx.message.author), value=textto("game1-cpup",ctx.message.author))
                    await guide.edit(embed=embed)
                elif str(reaction.emoji) == str(bot.get_emoji(653161518334214144)):
                    break
                else:
                    await ctx.send(textto("game1-notr",ctx.message.author))
            tmfin = 21 - tmint
            ufin = 21 - uint
            u = str(uint)
            sn=str(tmint)
            if 21 >= uint and tmfin > ufin or 21 < tmint and 21 >= uint:
                win=textto("game1-yourwin",ctx.message.author)
            elif 21 >= tmint and tmfin < ufin or 21 < uint and 21>= tmint:
                win=textto("game1-sinawin",ctx.message.author)
            else:
                win=textto("game1-dr",ctx.message.author)
            embed = discord.Embed(title=textto("game1-fin1",ctx.message.author).format(win), description=textto("game1-fin2",ctx.message.author).format(u,sn), color=ec)
            await guide.edit(embed=embed)
        else:
            if user2.bot:
                await ctx.send(textto("game1-vsbot",ctx.message.author))
                return
            if user2 == ctx.author:
                join=await ctx.send(textto("game1-join-anyone",ctx.message.author))
                await join.add_reaction(bot.get_emoji(653161519206629386))
                await join.add_reaction(bot.get_emoji(653161518833074178))
                try:
                    r,u= await bot.wait_for("reaction_add", check=lambda r,u: str(r.emoji) in [str(bot.get_emoji(653161519206629386)),str(bot.get_emoji(653161518833074178))] and r.message.id==join.id and u.bot==False,timeout=60)
                except:
                    await ctx.send(textto("game1-timeouted",ctx.message.author))
                    return
            else:
                join=await ctx.send(textto("game1-join",ctx.message.author).format(user2.mention))
                await join.add_reaction(bot.get_emoji(653161519206629386))
                await join.add_reaction(bot.get_emoji(653161518833074178))
                try:
                    r,u= await bot.wait_for("reaction_add", check=lambda r,u: str(r.emoji) in [str(bot.get_emoji(653161519206629386)),str(bot.get_emoji(653161518833074178))] and r.message.id==join.id and u == user2,timeout=60)
                except:
                    await ctx.send(textto("game1-timeouted",ctx.message.author))
                    return
            if str(r.emoji)==str(bot.get_emoji(653161519206629386)):
                u1 = ctx.message.author
                u1_dm = await opendm(u1)
                u1_card = 0
                u1_pass = False
                u2 = u
                u2_dm = await opendm(u2)
                u2_card = 0
                u2_pass = False
                e1 = discord.Embed(title=textto("game1-vs-et",u1),description=textto("game1-vs-ed",u1).format(str(u1),str(u2)),color=ec)
                e2 = discord.Embed(title=textto("game1-vs-et",u2),description=textto("game1-vs-ed",u2).format(str(u1),str(u2)),color=ec)
                await u1_dm.send(embed=e1)
                await u2_dm.send(embed=e2)
                while not(u1_pass and u2_pass):
                    u1_pass = False
                    u2_pass = False
                    u1_msg = await u1_dm.send(textto("game1-vs-yourturn",ctx.message.author).format(u1_card))
                    await u1_msg.add_reaction(bot.get_emoji(653161517927366658))
                    await u1_msg.add_reaction(bot.get_emoji(653161518334214144))
                    r,u=await bot.wait_for("reaction_add", check=lambda r,u: str(r.emoji) in [str(bot.get_emoji(653161517927366658)),str(bot.get_emoji(653161518334214144))] and r.message.id==u1_msg.id and u == u1)
                    if str(r.emoji)==str(bot.get_emoji(653161517927366658)):
                        u1_card  = u1_card + random.randint(1,11)
                        await u1_msg.edit(content=textto("game1-vs-dr",ctx.message.author).format(u1_card))
                    elif str(r.emoji)==str(bot.get_emoji(653161518334214144)):
                        u1_pass=True
                        await u1_msg.edit(content=textto("game1-vs-pass",ctx.message.author).format(u1_card))
                    u2_msg = await u2_dm.send(textto("game1-vs-yourturn",ctx.message.author).format(u2_card))
                    await u2_msg.add_reaction(bot.get_emoji(653161517927366658))
                    await u2_msg.add_reaction(str(bot.get_emoji(653161518334214144)))
                    r,u=await bot.wait_for("reaction_add", check=lambda r,u: str(r.emoji) in [str(bot.get_emoji(653161517927366658)),str(bot.get_emoji(653161518334214144))] and r.message.id==u2_msg.id and u == u2)
                    if str(r.emoji)==str(bot.get_emoji(653161517927366658)):
                        u2_card  = u2_card + random.randint(1,11)
                        await u2_msg.edit(content=textto("game1-vs-dr",ctx.message.author).format(u2_card))
                    elif str(r.emoji)==str(bot.get_emoji(653161518334214144)):
                        u2_pass=True
                        await u2_msg.edit(content=textto("game1-vs-pass",ctx.message.author).format(u2_card))
                u1_fin = 21 - u1_card
                u2_fin = 21 - u2_card
                if 21 >= u1_card and u2_fin > u1_fin or 21 < u2_card and 21 >= u1_card:
                    await ctx.send(textto("game1-vs-fin-win",ctx.message.author).format(u1.mention))
                elif 21 >= u2_card and u2_fin < u1_fin or 21 < u1_card and 21>= u2_card:
                    await ctx.send(textto("game1-vs-fin-win",ctx.message.author).format(u2.mention))
                else:
                    await ctx.send(textto("game1-vs-fin-draw",ctx.message.author))
                await ctx.send(textto("game1-vs-res",ctx.message.author).format(u1.mention,u1_card,u2.mention,u2_card))
            else:
                await ctx.send(textto("game1-cancel",ctx.message.author).format(ctx.author.mention))
    else:
        try:
            await ctx.send(embed=discord.Embed(title=textto("dhaveper",ctx.message.author),description=textto("per-manamsg",ctx.message.author)))
        except:
             await ctx.send(f'{textto("dhaveper",ctx.message.author)}\n{textto("per-manamsg",ctx.message.author)}')


@bot.command()
async def game2(ctx):

    answer = random.randint(1,100)
    await ctx.send(textto("game2-ready",ctx.message.author))
    i=0
    while True:
        try:
            msg = await bot.wait_for('message', check=lambda m: m.author==ctx.author and m.channel==ctx.channel,timeout=60)
        except:
            await ctx.send(textto("game2-timeout",ctx.message.author).format(answer))
            return
        try:
            i = i + 1
            ur = int(msg.content)
        except:
            await ctx.send(f"{ctx.author.mention}\n{textto('game2-notint',ctx.message.author)}")
            continue
        if ur>answer:
            await ctx.send(f'{ctx.author.mention}\n{textto("game2-high",ctx.message.author)}')
        elif ur<answer:
            await ctx.send(f'{ctx.author.mention}\n{textto("game2-low",ctx.message.author)}')
        else:
            await ctx.send(f'{ctx.author.mention}\n{textto("game2-clear",ctx.message.author).format(i)}')
            break
    

@bot.command()
async def changenick(ctx, name=None):
    print(f'{ctx.message.author.name}({ctx.message.guild.name})_'+ ctx.message.content )
    if ctx.message.author.id == 404243934210949120:
        await ctx.message.guild.me.edit(nick=name)
        if name == None:
            await ctx.send("私のニックネームをデフォルトの名前に変更したよ。")
        else:
            await ctx.send("私のニックネームを"+name+"に変更したよ。")
    else:
        await ctx.send("このコマンドはmii-10さんが私にニックネームを変更するときに使うものだよ！")

@bot.command()
async def Wecall(ctx, us=None, name=None):

    print(f'{ctx.message.author.name}({ctx.message.guild.name})_'+ ctx.message.content )
    if not us == None and not name == None:
        if not ctx.message.mentions[0].id == ctx.author.id:
            if ctx.message.mentions[0].bot == False:
                ok = await ctx.send(textto("Wecall-areyouok",ctx.message.author).format(ctx.message.mentions[0].mention,ctx.message.author.mention,name))
                await ok.add_reaction('⭕')
                await ok.add_reaction('❌')
                reaction, user = await bot.wait_for("reaction_add", check=lambda r,u: r.message.id==ok.id and u.id == ctx.message.mentions[0].id)
                if str(reaction.emoji) == "⭕":
                    try:
                        await ctx.message.mentions[0].edit(nick=name)
                        await ctx.send(textto("Wecall-changed",ctx.message.author))
                    except:
                        await ctx.send(textto("Wecall-notchanged1",ctx.message.author))
                else:
                    await ctx.send(textto("Wecall-notchanged2",ctx.message.author))
            else:
                await ctx.send(textto("Wecall-bot",ctx.message.author))
        else:
            await ctx.send(textto("Wecall-not",ctx.message.author))


@bot.command()
async def QandA(ctx):

    print(f'{ctx.message.author.name}({ctx.message.guild.name})_'+ ctx.message.content )
    quest = len(ctx.message.content.replace("s-QandA ","")) % 5
    if quest == 0:
        await ctx.send("yes")
    elif quest == 1:
       await ctx.send("no")
    elif quest == 2:
       await ctx.send("no")
    elif quest == 3:
       await ctx.send("yes")
    elif quest == 4:
       await ctx.send("?")

@bot.command()
@commands.cooldown(1, 5, type=commands.BucketType.user)
async def eatit(ctx,it):

    print(f'{ctx.message.author.name}({ctx.message.guild.name})_'+ ctx.message.content )
    if textto("language",ctx.author)=="ja":
        if textto(f"eat-{it}",ctx.message.author).startswith("Not found key:"):
            await ctx.send(textto("eat-?",ctx.message.author))
        else:
            await ctx.send(textto(f"eat-{it}",ctx.message.author))
    else:
        await ctx.send(textto("cannot-run",ctx.author))

@bot.command(aliases=["ユーザー情報","ユーザーの情報を教えて"])
async def userinfo(ctx, mus:commands.MemberConverter=None):

    print(f'{ctx.message.author.name}({ctx.message.guild.name})_'+ ctx.message.content )
    if mus == None:
        info = ctx.message.author
    else:
        info = mus
    async with ctx.message.channel.typing(): 
        if info.id in [i[1] for i in partnerg]:
            ptn="🔗パートナーサーバーオーナー:"
        else:
            ptn=""
        if ctx.guild.owner == info:
            embed = discord.Embed(title=textto("userinfo-name",ctx.message.author), description=f"{ptn}{info.name} - {ondevicon(info)} - {textto('userinfo-owner',ctx.message.author)}", color=info.color)
        else:
            embed = discord.Embed(title=textto("userinfo-name",ctx.message.author), description=f"{ptn}{info.name} - {ondevicon(info)}", color=info.color)
        try:
            if not info.premium_since is None:
                embed.add_field(name=textto("userinfo-guildbooster",ctx.message.author), value=f"since {info.premium_since}")
        except:
            pass
        embed.add_field(name=textto("userinfo-joindiscord",ctx.message.author), value=info.created_at)
        embed.add_field(name=textto("userinfo-id",ctx.message.author), value=info.id)
        embed.add_field(name=textto("userinfo-online",ctx.message.author), value=f"{str(info.status)}")
        embed.add_field(name=textto("userinfo-isbot",ctx.message.author), value=str(info.bot))
        embed.add_field(name=textto("userinfo-displayname",ctx.message.author), value=info.display_name)
        embed.add_field(name=textto("userinfo-joinserver",ctx.message.author), value=info.joined_at)
        if not info.activity == None:
            try:
                if info.activity.name == "Custom Status":
                    embed.add_field(name=textto("userinfo-nowplaying",ctx.message.author), value=f'{info.activity.state}')
                else:
                    embed.add_field(name=textto("userinfo-nowplaying",ctx.message.author), value=f'{info.activity.name}')
            except:
                embed.add_field(name=textto("userinfo-nowplaying",ctx.message.author), value=info.activity)
        hasroles = ""
        for r in info.roles:
            hasroles = hasroles + f"{r.mention},"
        embed.add_field(name=textto("userinfo-roles",ctx.message.author), value=hasroles)
        embed.add_field(name="guild permissions",value=f"`{'`,`'.join([i[0] for i in list(info.guild_permissions) if i[1]])}`")
        if not info.avatar_url == None:
            embed.set_thumbnail(url=info.avatar_url_as(static_format='png'))
            embed.add_field(name=textto("userinfo-iconurl",ctx.message.author),value=info.avatar_url_as(static_format='png'))
        else:
            embed.set_image(url=info.default_avatar_url_as(static_format='png'))
    await ctx.send(embed=embed)

@bot.command(aliases=["rt"])
@commands.cooldown(1, 5, type=commands.BucketType.user)
async def rettext(ctx,*,te):

    print(f'{ctx.message.author.name}({ctx.message.guild.name})_'+ ctx.message.content )
    await ctx.send(te)
    await ctx.message.delete()

@bot.command()
@commands.is_owner()
async def retfmt(ctx):
    print(f'{ctx.message.author.name}({ctx.message.guild.name})_'+ ctx.message.content )
    try:
        await ctx.send(ctx.message.clean_content.replace("s-retfmt ","").format(ctx,bot).replace("第三・十勝チャット Japan(beta)",""))
    except Exception as e:
        await ctx.send(e)

@bot.command()
async def sendto(ctx,cid):

    print(f'{ctx.message.author.name}({ctx.message.guild.name})_'+ ctx.message.content )
    try:
        ch = bot.get_channel(int(cid))
        if ch == None:
            await ctx.send(textto("sendto-notfound",ctx.message.author))
        else:
            ctt = ctx.message.content.replace("s-sendto "+cid+" ","")
            embed = discord.Embed(title=ctt, description=ctx.message.guild.name.replace("第三・十勝チャット Japan(beta)","某サバ")+f"、{ctx.message.channel.name}より", color=ctx.message.author.color)
            embed.set_author(name=str(ctx.message.author), icon_url=ctx.message.author.avatar_url)
            sdctx = await ch.send(embed=embed)
            await ctx.send("以下の文面を送信しました。\n"+str(ctx.message.author)+":"+ctt)
            await ctx.message.delete()
            """await sdctx.add_reaction('💬')
            await asyncio.sleep(0.5)
            re = await bot.wait_for("reaction_add", check=lambda r,u: str(r.emoji) == "💬" and r.message.id==sdctx.id)
            ck = await ctx.send("返信したい人がいるよ、チャンネルIDを送るなら⭕リアクションしてね、")
            ckr = await bot.wait_for("reaction_add", check=lambda r,u: str(r.emoji) == "⭕️" and r.message.id==ck.id)
            await bot.send_message(ch,f"返信用のチャンネルID:{ctx.message.channel.id}")"""
    except:
        await ctx.message.delete()
        await ctx.send(textto("sendto-except",ctx.message.author))

@bot.command(aliases=["メッセージ一括削除","次の件数分、メッセージを消して"])
@commands.cooldown(1, 15, type=commands.BucketType.guild)
async def delmsgs(ctx,msgcount):

    if ctx.message.author.permissions_in(ctx.message.channel).manage_messages == True or ctx.author.id == 404243934210949120:
        async with ctx.message.channel.typing():
            print(f'{ctx.message.author.name}({ctx.message.guild.name})_'+ ctx.message.content )
            dmc = ctx.message
            await dmc.delete()
            dr=await dmc.channel.purge(limit=int(msgcount))
            await ctx.send(textto("delmsgs-del",ctx.message.author).format(len(dr)))

@bot.command(aliases=["ステータス","あなたの情報を教えて"])
async def status(ctx):

    print(f'{ctx.message.author.name}({ctx.message.guild.name})_'+ ctx.message.content )
    embed = discord.Embed(title=textto("status-inserver",ctx.message.author), description=f"{len(bot.guilds)}", color=ec)
    embed.add_field(name=textto("status-prefix",ctx.message.author), value="s-")
    embed.add_field(name=textto("status-starttime",ctx.message.author), value=StartTime)
    embed.add_field(name=textto("status-ver",ctx.message.author), value=platform.python_version())
    embed.add_field(name=textto("status-pros",ctx.message.author), value=platform.processor())
    embed.add_field(name=textto("status-os",ctx.message.author), value=f"{platform.system()} {platform.release()}({platform.version()})")
    await ctx.send(embed=embed)

@bot.command()
async def gchinfo(ctx,name="main"):
    cursor.execute("select * from globalchs where name = ?",(name,))
    chs = cursor.fetchone()
    if chs["ids"]:
        retchs = ""
        for ch in chs["ids"]:
            try:
                retchs = f"{retchs}{bot.get_channel(ch).guild.name},{bot.get_channel(ch).name}\n"
            except:
                retchs = f"{retchs}不明なサーバー,チャンネルID:{ch}\n"
        await ctx.send(embed=getEmbed(f"グローバルチャンネル{name}の詳細",f"コネクトされたチャンネルとサーバー\n{retchs}",ec))
    else:
        await ctx.send("そのグローバルチャンネルはありません。")

@bot.command(aliases=["フィードバック","開発者にフィードバックを送って"])
async def feedback(ctx,ttl,ctt=None):

    embed = discord.Embed(title=ttl, description=ctt, color=ec)
    fbc = bot.get_channel(532497710649966592)
    embed.set_author(name=f"{str(ctx.message.author)}", icon_url=ctx.message.author.avatar_url_as(static_format='png'))
    await fbc.send(embed=embed)
    await ctx.send(textto("feedback-sended",ctx.message.author))

@bot.command(aliases=["レポート","報告","通報","お知らせ"])
async def report(ctx,ttl,*,ctt=None):

    embed = discord.Embed(title=ttl, description=ctt, color=ec)
    fbc = bot.get_channel(564353126770016256)
    embed.set_author(name=f"{str(ctx.message.author)}", icon_url=ctx.message.author.avatar_url_as(static_format='png'))
    await fbc.send(embed=embed)
    await ctx.send(textto("thanks-report",ctx.author))

@bot.command(aliases=["オンライン状況","次の人のオンライン状況を教えて"])
async def isonline(ctx,uid:int=None):

    print(f'{ctx.message.author.name}({ctx.message.guild.name})_'+ ctx.message.content )
    if uid==None:
        cid = ctx.message.author.id
    else:
        cid = uid
    async with ctx.message.channel.typing():
        for guild in bot.guilds:
            u = guild.get_member(uid)
            if not u == None:
                break
    if not u == None:
        await ctx.send(textto("ison-now",ctx.message.author).format(u.name,str(u.status)))
    else:
        await ctx.send(textto("ison-notfound",ctx.message.author))

@bot.command()
async def changeRPC(ctx,text=None):
    if ctx.message.author.id == 404243934210949120:
        if text==None:
            await bot.change_presence(activity=discord.Game(name=f'ヘルプ:"s-help"|起動時サバ数:{len(bot.guilds)}|アイコン:まじすたさん'))
        else:
            await bot.change_presence(activity=discord.Game(name=text))
        await ctx.send("変更しました。")

@bot.command()
async def allonline(ctx,mus=None):

    print(f'{ctx.message.author.name}({ctx.message.guild.name})_'+ ctx.message.content )
    if mus == None:
        info = ctx.message.author
    else:
        if ctx.message.mentions:
            info = ctx.message.mentions[0]
        else:
            info = ctx.guild.get_member(int(mus))
    await ctx.send(f"Status:{str(info.status)}(PC:{str(info.desktop_status)},Mobile:{str(info.mobile_status)},Web:{str(info.web_status)})")

@bot.command(aliases=["レベルカード切替","次の番号のカードにレベルカードを切り替えて"])
async def switchlevelcard(ctx,number:int=None):

    cursor.execute("select * from users where id=?",(ctx.author.id,))
    upf = cursor.fetchone()
    cn=["kazuta123-a","kazuta123-b","m@ji☆","tomohiro0405","氷河","雪銀　翔","kazuta123-c"]
    if number==None:
        await ctx.send(textto("slc-your",ctx.message.author).format(upf["levcard"].replace("-a","").replace("-b","").replace("-c","")))
    else:
        if 1 <= number <= 6:
            await ctx.send(textto("slc-set",ctx.message.author).format(number,cn[number-1].replace("-a","").replace("-b","").replace("-c","")))
        else:
            await ctx.send(textto("slc-numb",ctx.message.author))
            cursor.execute("UPDATE users SET levcard = ? WHERE id = ?", (cn[number-1],ctx.author.id))

@bot.command(aliases=["クレジット","クレジットを見せて"])
async def credit(ctx):

    await ctx.send(textto("credit",ctx.message.author))

@bot.command(name="activity",aliases=["アクティビティ","なにしてるか見せて"])
@commands.cooldown(1, 5, type=commands.BucketType.user)
async def infoactivity(ctx, mus:commands.MemberConverter=None):
    print(f'{ctx.message.author.name}({ctx.message.guild.name})_'+ ctx.message.content )
    try:
        await bot.request_offline_members(ctx.guild)
    except:
        pass
    if mus is None:
        info = ctx.message.author
    else:
        info = mus
    if info.activity is None:
        if str(info.status) == "offline":
            embed = discord.Embed(title=textto("playinginfo-doing",ctx.message.author), description=textto("playinginfo-offline",ctx.message.author), color=info.color)
        else:
            sete =False
            try:
                if info.voice.self_stream:
                    embed = discord.Embed(title=textto("playinginfo-doing",ctx.message.author), description=str(bot.get_emoji(653161518250196992))+textto("playinginfo-GoLive",ctx.message.author), color=info.color)
                    sete=True
                elif info.voice.self_video:
                    embed = discord.Embed(title=textto("playinginfo-doing",ctx.message.author), description=str(bot.get_emoji(653161517960658945))+textto("playinginfo-screenshare",ctx.message.author), color=info.color)
                    sete=True
                elif info.voice:
                    embed = discord.Embed(title=textto("playinginfo-doing",ctx.message.author), description=str(bot.get_emoji(653161518082293770))+textto("playinginfo-invc",ctx.message.author), color=info.color)
                    sete=True
            except:
                pass
            if not sete:
                if info.bot:
                    embed = discord.Embed(title=textto("playinginfo-doing",ctx.message.author), description=textto("playinginfo-bot",ctx.message.author), color=info.color)
                elif "🌐"==ondevicon(info):
                    embed = discord.Embed(title=textto("playinginfo-doing",ctx.message.author), description=textto("playinginfo-onlyWeb",ctx.message.author), color=info.color)
                elif "📱"==ondevicon(info):
                    embed = discord.Embed(title=textto("playinginfo-doing",ctx.message.author), description=textto("playinginfo-onlyPhone",ctx.message.author), color=info.color)
                else:
                    embed = discord.Embed(title=textto("playinginfo-doing",ctx.message.author), description=textto("playinginfo-noActivity",ctx.message.author), color=info.color)
        activ=info.activity
        embed.set_author(name=info.display_name, icon_url=info.avatar_url_as(static_format='png'))
        await ctx.send(embed=embed)
    else:
        for anactivity in info.activities:
            if anactivity.type == discord.ActivityType.playing:
                activName=textto("playinginfo-playing",ctx.message.author)+anactivity.name
            elif anactivity.type == discord.ActivityType.watching:
                activName=textto("playinginfo-watching",ctx.message.author)+anactivity.name
            elif anactivity.type == discord.ActivityType.listening:
                activName=textto("playinginfo-listening",ctx.message.author).format(anactivity.name)
            elif anactivity.type ==  discord.ActivityType.streaming:
                activName=textto("playinginfo-streaming",ctx.message.author)+anactivity.name
            else:
                try:
                    if anactivity.name == "Custom Status":
                        activName=textto("playinginfo-custom_status",ctx.message.author)
                    else:
                        activName=textto("playinginfo-unknown",ctx.message.author)+anactivity.name
                except:
                    activName=textto("playinginfo-unknown",ctx.message.author)+anactivity.name
            embed = discord.Embed(title=textto("playinginfo-doing",ctx.message.author), description=activName, color=info.color)
            activ=anactivity
            embed.set_author(name=info.display_name, icon_url=info.avatar_url_as(static_format='png'))
            if anactivity.name == "Spotify":
                try:
                    embed.add_field(name=textto("playinginfo-title",ctx.message.author), value=activ.title)
                    embed.add_field(name=textto("playinginfo-artist",ctx.message.author), value=activ.artist)
                    embed.add_field(name=textto("playinginfo-album",ctx.message.author), value=activ.album)
                    embed.add_field(name="URL", value=f"https://open.spotify.com/track/{activ.track_id}")
                    #embed.add_field(name="経過時間", value=str(activ.duration.seconds/60)+str(activ.duration.seconds%60))
                    embed.set_thumbnail(url=activ.album_cover_url)
                except AttributeError:
                    embed.add_field(name="ローカルファイルの再生中", value="一緒に聞くことはできません！")
                    embed.add_field(name=textto("playinginfo-title",ctx.message.author), value=activ.details)
                    embed.add_field(name=textto("playinginfo-artist",ctx.message.author), value=activ.state)
            elif anactivity.type==discord.ActivityType.streaming:
                try:
                    embed.add_field(name=textto("playinginfo-streampage",ctx.message.author), value=activ.url)
                except:
                    pass
                try:
                    embed.add_field(name=textto("playinginfo-do",ctx.message.author), value=activ.datails)
                except:
                    pass
            else:
                try:
                    vl = ""
                    if activ.details:
                        vl = f"{activ.details}\n"
                    if activ.state:
                        vl = f"{vl}{activ.state}\n"
                    if vl == "":
                        vl = "なし"
                    embed.add_field(name=textto("playinginfo-det",ctx.message.author), value=vl)
                except:
                    pass
            await ctx.send(embed=embed)


@bot.command(aliases=["役職情報","次の役職について教えて"])
async def roleinfo(ctx,*,role:commands.RoleConverter=None):

    if role==None:
        await ctx.send(textto("roleinfo-howto",ctx.message.author))
    elif role.guild == ctx.guild:
        embed = discord.Embed(title=role.name, description=f"id:{role.id}", color=role.colour)
        embed.add_field(name=textto("roleinfo-hoist",ctx.message.author), value=role.hoist)
        embed.add_field(name=textto("roleinfo-mention",ctx.message.author), value=role.mentionable)
        hasmember=""
        for m in role.members:
            hasmember = hasmember + f"{m.mention},"
        if not hasmember == "":
            embed.add_field(name=textto("roleinfo-hasmember",ctx.message.author), value=hasmember)
        else:
            embed.add_field(name=textto("roleinfo-hasmember",ctx.message.author), value="(None)")
        hasper = ""
        for pn,bl in iter(role.permissions):
            if bl:
                hasper = hasper + f"`{pn}`,"
        embed.add_field(name=textto("roleinfo-hasper",ctx.message.author), value=hasper)
        embed.add_field(name=textto("roleinfo-created",ctx.message.author), value=role.created_at)

        await ctx.send(embed=embed)
    else:
        await ctx.send(textto("roleinfo-other",ctx.message.author))

@bot.command(aliases=["ボイス情報","音声情報を教えて"])
async def voiceinfo(ctx,mus:commands.MemberConverter=None):

    print(f'{ctx.message.author.name}({ctx.message.guild.name})_'+ ctx.message.content )
    if mus == None:
        info = ctx.message.author
    else:
        info = mus
    try:
        embed = discord.Embed(title=info.display_name, description=f"{info.voice.channel.guild.name} - {info.voice.channel.name}", color=info.colour)
        vste=""
        if info.voice.deaf:
            #サバスピーカーミュート
            vste=vste+str(bot.get_emoji(653161518057127937))
        else:
            #サバスピーカーオン
            vste=vste+str(bot.get_emoji(653161518082293770))
        if info.voice.mute:
            #サバマイクミュート
            vste=vste+str(bot.get_emoji(653161518086619137))
        else:
            #サバマイクオン
            vste=vste+str(bot.get_emoji(653161518086619137))
        if info.voice.self_deaf:
            #スピーカーミュート
            vste=vste+str(bot.get_emoji(653161518258585620))
        else:
            #スピーカーオン
            vste=vste+str(bot.get_emoji(653161517881098272))
        if info.voice.self_mute:
            #マイクミュート
            vste=vste+str(bot.get_emoji(653161519143714816))
        else:
            #マイクオン
            vste=vste+str(bot.get_emoji(653161518224900096))
        if info.voice.self_video:
            #画面共有
            vste=vste+str(bot.get_emoji(653161517960658945))
        elif info.voice.self_stream:
            #GoLive
            vste=vste+str(bot.get_emoji(653161518250196992))
        embed.add_field(name="ステータス(status)",value=vste)
    except AttributeError:
        await ctx.send(textto("vi-nfch",ctx.message.author))
    await ctx.send(embed=embed)

@bot.command(name="chinfo",aliases=["チャンネル情報","次のチャンネルについて教えて"])
async def channelinfo(ctx,cid:int=None):

    if cid is None:
        ch = ctx.message.channel
    else:
        ch = ctx.guild.get_channel(cid)
    if isinstance(ch,discord.TextChannel):

        embed = discord.Embed(title=ch.name, description=f"id:{ch.id}", color=ctx.author.colour)

        embed.add_field(name=textto("ci-type",ctx.message.author),value=textto("ci-text",ctx.message.author))

        embed.add_field(name=textto("ci-topic",ctx.message.author),value=str(ch.topic))

        embed.add_field(name=textto("ci-slow",ctx.message.author),value=str(ch.slowmode_delay).replace("0",textto("ci-None",ctx.message.author)))

        embed.add_field(name=textto("ci-nsfw",ctx.message.author),value=ch.is_nsfw())

        embed.add_field(name=textto("ci-cate",ctx.message.author),value=ch.category)

        embed.add_field(name=textto("ci-created",ctx.message.author),value=ch.created_at)

        embed.add_field(name=textto("ci-invitec",ctx.message.author),value=str(len(await ch.invites())).replace("0",textto("ci-None",ctx.message.author)))

        embed.add_field(name=textto("ci-pinc",ctx.message.author),value=str(len(await ch.pins())).replace("0",textto("ci-None",ctx.message.author)))

        embed.add_field(name=textto("ci-whc",ctx.message.author),value=str(len(await ch.webhooks())).replace("0",textto("ci-None",ctx.message.author)))

        embed.add_field(name=textto("ci-url",ctx.message.author),value=f"[{textto('ci-click',ctx.message.author)}](https://discordapp.com/channels/{ctx.guild.id}/{ch.id})")

        await ctx.send(embed=embed)

    elif isinstance(ch,discord.VoiceChannel):
        embed = discord.Embed(title=ch.name, description=f"id:{ch.id}", color=ctx.author.colour)

        embed.add_field(name=textto("ci-type",ctx.message.author),value=textto("ci-voice",ctx.message.author))

        embed.add_field(name=textto("ci-bit",ctx.message.author),value=ch.bitrate)

        embed.add_field(name=textto("ci-limituser",ctx.message.author),value=str(ch.user_limit).replace("0",textto("ci-None",ctx.message.author)))

        embed.add_field(name=textto("ci-cate",ctx.message.author),value=ch.category)

        embed.add_field(name=textto("ci-created",ctx.message.author),value=ch.created_at)

        embed.add_field(name=textto("ci-invitec",ctx.message.author),value=str(len(await ch.invites())).replace("0",textto("ci-None",ctx.message.author)))

        embed.add_field(name=textto("ci-url",ctx.message.author),value=f"[{textto('ci-click',ctx.message.author)}](https://discordapp.com/channels/{ctx.guild.id}/{ch.id})")

        await ctx.send(embed=embed)

    elif isinstance(ch,discord.CategoryChannel):
        
        embed = discord.Embed(title=ch.name, description=f"id:{ch.id}", color=ctx.author.colour)

        embed.add_field(name=textto("ci-type",ctx.message.author),value=textto("ci-cate",ctx.message.author))

        embed.add_field(name=textto("ci-nsfw",ctx.message.author),value=ch.is_nsfw())

        ic = ""

        for c in ch.channels:
            ic = ic + c.mention + ","

        embed.add_field(name=textto("ci-inch",ctx.message.author),value=ic)

        embed.add_field(name=textto("ci-created",ctx.message.author),value=ch.created_at)

        embed.add_field(name=textto("ci-url",ctx.message.author),value=f"[{textto('ci-click',ctx.message.author)}](https://discordapp.com/channels/{ctx.guild.id}/{ch.id})")

        await ctx.send(embed=embed)
    else:
        await ctx.send(textto("ci-notfound",ctx.message.author))


@bot.command(aliases=["アンケート","次のアンケートを開いて"])
async def q(ctx,title=None,*ctt):

    if title == None or ctt == []:
        await ctx.send(textto("q-not",ctx.message.author))
    else:
        ky=None
        dct = {}
        for tmp in ctt:
            if ky==None:
                ky = tmp
            else:
                dct[ky]=tmp
                ky = None
        itm = ""
        for k,v in dct.items():
            if itm == "":
                itm = f"{k}:{v}"
            else:
                itm = itm + f"\n{k}:{v}"
        embed = discord.Embed(title=title,description=itm)
        qes = await ctx.send(embed=embed)

        for k in ctt[::2]:
            try:
                await qes.add_reaction(k)
            except Exception as e:
                try:
                    eid = re.match("<:[a-zA-Z0-9_-]+:([0-9]+)>",k).group(1)
                    ej = bot.get_emoji(int(eid))
                    await qes.add_reaction(ej)
                except:
                    await qes.delete()
                    await ctx.send(textto("q-error",ctx.author))

@bot.command(aliases=["ピン留め切替","次のメッセージをピン留めして"])
async def pin(ctx,mid:int):

    msg = await ctx.message.channel.fetch_message(mid)
    if msg.pinned:
        await msg.unpin()
        await ctx.send(textto("pin-unpinned",ctx.message.author))
    else:
        await msg.pin()
        await ctx.send(textto("pin-pinned",ctx.message.author))


@bot.command(aliases=["バン","次のメンバーをこのサーバーからbanして"])
@commands.cooldown(1, 10, type=commands.BucketType.guild)
async def memban(ctx,mem:int,dmd:int=0,rs=None):

    user_per = ctx.channel.permissions_for(ctx.author).ban_members
    bot_per = ctx.channel.permissions_for(ctx.guild.me).ban_members
    if user_per and bot_per or ctx.author.id == 404243934210949120:
        try:
            bmem = await bot.fetch_user(mem)
            await ctx.guild.ban(bmem,delete_message_days=dmd,reason=rs)
        except:
            await ctx.send(textto("mem-up",ctx.message.author))
        else:
            await ctx.send(textto("mem-banned",ctx.message.author))
    else:
        await ctx.send(textto("mem-don'thasper",ctx.message.author))



@bot.command(aliases=["キック","次のメンバーをこのサーバーから追い出して"])
@commands.cooldown(1, 5, type=commands.BucketType.guild)
async def memkick(ctx,mem:commands.MemberConverter):

    user_per = ctx.channel.permissions_for(ctx.author).kick_members
    bot_per = ctx.channel.permissions_for(ctx.guild.me).kick_members
    if user_per and bot_per or ctx.author.id == 404243934210949120:
        try:
            await mem.kick()
        except:
            await ctx.send(textto("mem-up",ctx.message.author))
        else:
            await ctx.send(textto("mem-kicked",ctx.message.author))
    else:
        await ctx.send(textto("mem-don'thasper",ctx.message.author))

@bot.command(aliases=["次のボイスチャンネルのURLを教えて"])
async def vcurl(ctx,vch:commands.VoiceChannelConverter=None):

    if vch is None and (not ctx.author.voice == None):
        ch = ctx.author.voice.channel
    else:
        ch = vch
    await ctx.send(embed=getEmbed(ch.name,f"https://discordapp.com/channels/{ctx.guild.id}/{ch.id}"))

@bot.command(aliases=["twitter検索","twitterで検索して"])
@commands.cooldown(1, 15, type=commands.BucketType.user)
async def twisearch(ctx,*,word:str):
    try:
        async with ctx.message.channel.typing():
            ret = twi.search.tweets(q=word,result_type="recent", lang="ja", count=2)
            tweet = ret["statuses"][0]
            embed = discord.Embed(description=tweet["text"], color=int(tweet["user"]["profile_background_color"],16))
            embed.set_author(name=f'{tweet["user"]["name"]}(@{tweet["user"]["screen_name"]})',url=f'https://twitter.com/{tweet["user"]["screen_name"]}', icon_url=tweet["user"]["profile_image_url_https"])
            try:
                embed.set_image(url=tweet["entities"]["media"][0]["media_url_https"])
            except:
                pass
            embed.add_field(name=textto("twi-see",ctx.message.author),value=f'{bot.get_emoji(653161518451392512)} https://twitter.com/{tweet["user"]["screen_name"]}/status/{tweet["id"]}')
        await ctx.send(embed=embed)
    except:
        await ctx.send(textto("twi-error",ctx.message.author))
        #await ctx.send(embed=getEmbed("traceback",traceback.format_exc(3)))

@bot.command()
async def rq(ctx):

    await ctx.send(f"{ctx.author.mention}"+textto("IllQ",ctx.author)+f"\n{random.choice(cmdqest)}")

@bot.command(name="Af")
async def a_01(ctx):
    if not textto("language",ctx.author)=="ja":
        await ctx.send(textto("cannot-run",ctx.author))
        return

    await ctx.send(ctx.author.mention,embed=getEmbed("",f'あなたは「{random.choice(ctx.guild.members).display_name.replace(ctx.guild.me.display_name,"私").replace(ctx.author.display_name,"あなた自身")}」のこと、好きかな？'))

@bot.command(name="checkscrauname")
@commands.cooldown(1, 5, type=commands.BucketType.user)
async def scrauname(ctx, un:str):
    if not textto("language",ctx.author)=="ja":
        await ctx.send(textto("cannot-run",ctx.author))
        return

    print(f'{ctx.message.author.name}({ctx.message.guild.name})_'+ ctx.message.content )
    try:
        async with ctx.message.channel.typing():
            url = f'https://scratch.mit.edu/accounts/check_username/{un}'
            response = urllib.request.urlopen(url)
            content = json.loads(response.read().decode('utf8'))
            print(content)
        await ctx.send(embed=discord.Embed(title=f"Scratchでのユーザー名:\'{content[0]['username']}\'の使用可能状態",description=f"{content[0]['msg']}({content[0]['msg'].replace('username exists','存在するため使用不可').replace('bad username','検閲により使用不可').replace('invalid username','無効なユーザー名').replace('valid username','使用可能')})"))
    except:
        await ctx.send("何らかの例外が発生しました。")

@bot.command()
async def dmember(ctx,*,mus=None):
    if ctx.author.id == 404243934210949120:
        info=None
        tmp2=None
        if mus == None:
            await ctx.send("メンバーid/名前の指定は必須です。")
        else:
            tmp = None
            try:
                tmp = int(mus)
            except:
                pass
            for guild in bot.guilds:
                if tmp:
                    tmp2 = guild.get_member(int(mus))
                else:
                    tmp2 = guild.get_member_named(mus)
                if tmp2:
                    info = tmp2
                    break
        if info:
            async with ctx.message.channel.typing(): 
                if ctx.guild.owner == info:
                    embed = discord.Embed(title=textto("userinfo-name",ctx.message.author), description=f"{info.name} - {ondevicon(info)} - {textto('userinfo-owner',ctx.message.author)}", color=info.color)
                else:
                    embed = discord.Embed(title=textto("userinfo-name",ctx.message.author), description=f"{info.name} - {ondevicon(info)}", color=info.color)
                embed.add_field(name=textto("userinfo-joindiscord",ctx.message.author), value=info.created_at)
                embed.add_field(name=textto("userinfo-id",ctx.message.author), value=info.id)
                embed.add_field(name=textto("userinfo-online",ctx.message.author), value=f"{str(info.status)}")
                embed.add_field(name=textto("userinfo-isbot",ctx.message.author), value=str(info.bot))
                embed.add_field(name=textto("userinfo-displayname",ctx.message.author), value=info.display_name)
                embed.add_field(name=textto("userinfo-joinserver",ctx.message.author), value=info.joined_at)
                embed.add_field(name="サーバー", value=info.name)
                if not info.activity == None:
                    try:
                        embed.add_field(name=textto("userinfo-nowplaying",ctx.message.author), value=f'{info.activity.name}')
                    except:
                        embed.add_field(name=textto("userinfo-nowplaying",ctx.message.author), value=info.activity)
                hasroles = ""
                for r in info.roles:
                    hasroles = hasroles + f"{r.mention},"
                embed.add_field(name=textto("userinfo-roles",ctx.message.author), value=hasroles)
                if not info.avatar_url == None:
                    embed.set_thumbnail(url=info.avatar_url_as(static_format='png'))
                    embed.add_field(name=textto("userinfo-iconurl",ctx.message.author),value=info.avatar_url_as(static_format='png'))
                else:
                    embed.set_image(url=info.default_avatar_url_as(static_format='png'))
            await ctx.send(embed=embed)
        else:
            await ctx.send("一致するユーザーが、共通サーバーに見つかりませんでした。")

@bot.command()
async def checkmember(ctx,member:commands.MemberConverter):
    if not textto("language",ctx.author)=="ja":
        await ctx.send(textto("cannot-run",ctx.author))
        return

    bunotif = 0
    for g in bot.guilds:
        try:
            tmp = await g.bans()
        except:
            continue
        banulist = [i.user.id for i in tmp]
        if member.id in banulist:
            bunotif = bunotif + 1
    if bunotif == 0:
        await ctx.send(embed=discord.Embed(title=f"{member}の安全性評価",description=f"そのユーザーは、思惟奈ちゃんのいるサーバーでは、banされていません。"))
    else:
        await ctx.send(embed=discord.Embed(title=f"{member}の安全性評価",description=f"そのユーザーは、思惟奈ちゃんのいる{bunotif}のサーバーでbanされています。注意してください。"))


bot.remove_command('help')

@bot.command(aliases=["ヘルプ","できること見せて"])
async def help(ctx,rcmd=None):
    #ヘルプ内容
    if rcmd == None:
        page = 1
        embed = discord.Embed(title=textto("help-1-t",ctx.message.author), description=textto("help-1-d",ctx.message.author), color=ec)
        embed.set_footer(text=f"page:{page}")
        msg = await ctx.send(embed=embed)
        await msg.add_reaction(bot.get_emoji(653161518195671041))
        await msg.add_reaction(bot.get_emoji(653161518170505216))
        await msg.add_reaction("🔍")
        while True:
            try:
                r, u = await bot.wait_for("reaction_add", check=lambda r,u: r.message.id==msg.id and u.id == ctx.message.author.id,timeout=30)
            except:
                break
            try:
                await msg.remove_reaction(r,u)
            except:
                pass
            if str(r) == str(bot.get_emoji(653161518170505216)):
                if page == 14:
                    page = 1
                else:
                    page = page + 1
                embed = discord.Embed(title=textto(f"help-{page}-t",ctx.message.author), description=textto(f"help-{page}-d",ctx.message.author), color=ec)
                embed.set_footer(text=f"page:{page}")
                await msg.edit(embed=embed)
            elif str(r) == str(bot.get_emoji(653161518195671041)):
                if page == 1:
                    page = 14
                else:
                    page = page - 1
                embed = discord.Embed(title=textto(f"help-{page}-t",ctx.message.author), description=textto(f"help-{page}-d",ctx.message.author), color=ec)
                embed.set_footer(text=f"page:{page}")
                await msg.edit(embed=embed)
            elif str(r) == "🔍":
                await msg.remove_reaction(bot.get_emoji(653161518195671041),bot.user)
                await msg.remove_reaction("🔍",bot.user)
                await msg.remove_reaction(bot.get_emoji(653161518170505216),bot.user)
                qm = await ctx.send(textto("help-s-send",ctx.author))
                try:
                    msg = await bot.wait_for('message', check=lambda m: m.author==ctx.author and m.channel==ctx.channel,timeout=60)
                    sewd = msg.content
                except asyncio.TimeoutError:
                    pass
                else:
                    try:
                        await msg.delete()
                        await qm.delete()
                    except:
                        pass
                    async with ctx.message.channel.typing():
                        lang = textto("language",ctx.author)
                        with open(f"lang/{lang}.json","r",encoding="utf-8") as j:
                            f = json.load(j)
                        sre = discord.Embed(title=textto("help-s-ret-title",ctx.author),description=textto("help-s-ret-desc",ctx.author).format(sewd),color=ec)
                        for k,v in f.items():
                            if k.startswith("h-"):
                                if sewd in k.replace("h-","")  or sewd in v:
                                    sre.add_field(name=k.replace("h-",""),value=v.replace(sewd,f"**{sewd}**"))
                    await ctx.send(embed=sre)
        await msg.remove_reaction(bot.get_emoji(653161518195671041),bot.user)
        await msg.remove_reaction("🔍",bot.user)
        await msg.remove_reaction(bot.get_emoji(653161518170505216),bot.user)
    else:
        embed = discord.Embed(title=str(rcmd), description=textto(f"h-{str(rcmd)}",ctx.message.author), color=ec)
        if embed.description.startswith("Not found key:") or embed.description.startswith("Not found language:"):
            await ctx.send(textto("h-notfound",ctx.message.author))
        else:
            await ctx.send(embed=embed)

@bot.command(aliases=["r","返信","引用"])
async def reply(ctx,id:int,*,text):

    m = await ctx.channel.fetch_message(id)
    e = discord.Embed(description=text,color=ec)
    e.add_field(name=f"引用投稿(引用された投稿の送信者:{m.author.display_name})",value=f"{m.content}\n[{bot.get_emoji(653161518451392512)} この投稿に飛ぶ]({m.jump_url})")
    e.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar_url_as(static_format='png'))
    await ctx.send(embed=e)
    await ctx.message.delete()

@bot.command()
async def comlock(ctx,do="view",comname=""):
    cursor.execute("select * from guilds where id=?",(ctx.guild.id,))
    gs = cursor.fetchone()
    if do =="add":
        if not (ctx.author.guild_permissions.administrator or ctx.author.id == 404243934210949120):
            await ctx.send(textto("need-admin",ctx.author))
            return
        if not comname in gs["lockcom"]:
            gs["lockcom"].append(comname)
            cursor.execute("UPDATE guilds SET lockcom = ? WHERE id = ?", (gs["lockcom"],ctx.guild.id))
        await ctx.send(textto("upf-add",ctx.author).format(comname))
    elif do =="del":
        if not (ctx.author.guild_permissions.administrator or ctx.author.id == 404243934210949120):
            await ctx.send(textto("need-admin",ctx.author))
            return
        if comname in gs["lockcom"]:
            gs["lockcom"].remove(comname)
            cursor.execute("UPDATE guilds SET lockcom = ? WHERE id = ?", (gs["lockcom"],ctx.guild.id))
        await ctx.send(textto("deleted-text",ctx.author))
    elif do =="view":
        await ctx.send(textto("comlock-view",ctx.author).format(str(gs["lockcom"])))
    else:
        await ctx.send(textto("comlock-unknown",ctx.author))

@bot.command()
async def cprofile(ctx,usid=None):
    uid = usid or ctx.author.id
    cursor.execute("select * from users where id=?",(uid,))
    pf = cursor.fetchone()
    e = discord.Embed(title=textto("cpro-title",ctx.author),description=f"id:{uid}")
    e.add_field(name="prefix",value=pf["prefix"])
    e.add_field(name=textto("cpro-gpoint",ctx.author),value=pf["gpoint"])
    e.add_field(name=textto("cpro-levelcard",ctx.author),value=pf["levcard"])
    e.add_field(name=textto("cpro-renotif",ctx.author),value=pf["onnotif"])
    e.add_field(name=textto("cpro-lang",ctx.author),value=pf["lang"])
    await ctx.send(embed=e)

@bot.command()
@commands.is_owner()
async def aev(ctx,*,cmd):
    try:
        await eval(cmd)
    except:
        await ctx.send(embed=discord.Embed(title="awaitEvalエラー",description=traceback.format_exc(0)))

@bot.command(name="dguild")
async def serverinfo(ctx,sid=None):
    print(f'{ctx.message.author.name}({ctx.message.guild.name})_'+ ctx.message.content )
    if not sid == None:
        sevinfo = bot.get_guild(int(str(sid)))
    else:
        sevinfo = ctx.message.guild
    if sevinfo.id in [i[0] for i in partnerg]:
        ptn="🔗パートナーサーバー:"
    else:
        ptn=""
    try:
        embed = discord.Embed(title=textto("serverinfo-name",ctx.message.author), description=sevinfo.name, color=ec)
        if not sevinfo.icon_url == None:
            embed.set_thumbnail(url=sevinfo.icon_url_as(static_format='png'))
        embed.add_field(name=textto("serverinfo-role",ctx.message.author), value=len(sevinfo.roles))
        embed.add_field(name=textto("serverinfo-emoji",ctx.message.author), value=len(sevinfo.emojis))
        embed.add_field(name=textto("serverinfo-country",ctx.message.author), value=str(sevinfo.region))
        bm = 0
        ubm = 0
        for m in sevinfo.members:
            if m.bot:
                bm = bm + 1
            else:
                ubm = ubm + 1
        embed.add_field(name=textto("serverinfo-member",ctx.message.author), value=f"{len(sevinfo.members)}(bot:{bm}/user:{ubm})")
        embed.add_field(name=textto("serverinfo-channel",ctx.message.author), value=f'{textto("serverinfo-text",ctx.message.author)}:{len(sevinfo.text_channels)}\n{textto("serverinfo-voice",ctx.message.author)}:{len(sevinfo.voice_channels)}')
        embed.add_field(name=textto("serverinfo-id",ctx.message.author), value=sevinfo.id)
        embed.add_field(name=textto("serverinfo-owner",ctx.message.author), value=sevinfo.owner.name)
        embed.add_field(name=textto("serverinfo-create",ctx.message.author), value=sevinfo.created_at)
        rlist = ",".join([i.name for i in sevinfo.roles])
        if len(rlist) <= 1000:
            embed.add_field(name=textto("serverinfo-roles",ctx.message.author),value=rlist)
        try:
            embed.add_field(name=textto("serverinfo-nitroboost",ctx.message.author),value=textto("serverinfo-nitroboost-val",ctx.message.author).format(sevinfo.premium_tier))
            embed.add_field(name=textto("serverinfo-nitroboost-can-title",ctx.message.author),value=textto(f"serverinfo-nitroboost-can-{sevinfo.premium_tier}",ctx.message.author).format(sevinfo.premium_tier,sevinfo.premium_subscription_count))
        except:
            pass
        
        if sevinfo.system_channel:
            embed.add_field(name=textto("serverinfo-sysch",ctx.message.author),value=sevinfo.system_channel)
            try:
                embed.add_field(name=textto("serverinfo-sysch-welcome",ctx.message.author),value=sevinfo.system_channel_flags.join_notifications)
                embed.add_field(name=textto("serverinfo-sysch-boost",ctx.message.author),value=sevinfo.system_channel_flags.premium_subscriptions)
            except:
                pass
        if sevinfo.afk_channel:
            embed.add_field(name=textto("serverinfo-afkch",ctx.message.author),value=sevinfo.afk_channel.name)
            embed.add_field(name=textto("serverinfo-afktimeout",ctx.message.author),value=str(sevinfo.afk_timeout/60))
        await ctx.send(embed=embed)
    except Exception as e:
        await ctx.send(e)
        #await ctx.send(textto("serverinfo-except",ctx.message.author))


@bot.command(aliases=["言語設定","言語を次の言語に変えて"])
@commands.cooldown(1, 10, type=commands.BucketType.user)
async def userlang(ctx,lang):
    print(f'{ctx.message.author.name}({ctx.message.guild.name})_'+ ctx.message.content )
    if textto("language",lang).startswith("Not found language:"):
        await ctx.send(textto("setl-cantuse",ctx.author))
    else:
        cursor.execute("UPDATE users SET lang = ? WHERE id = ?", (lang,ctx.author.id))
        await ctx.send(textto("setl-set",ctx.message.author))


@bot.event
async def on_command_error(ctx, error):
    global DoServercmd
    """if isinstance(error, commands.CommandNotFound):
        if not DoServercmd:
            embed = discord.Embed(title=textto("cmd-error-t",ctx.message.author), description=textto("cmd-notfound-d",ctx.message.author), color=ec)
            DoServercmd = False
            await ctx.send(embed=embed)
    el"""
    if isinstance(error,commands.CommandOnCooldown):
        #クールダウン
        embed = discord.Embed(title=textto("cmd-error-t",ctx.message.author), description=textto("cmd-cooldown-d",ctx.message.author).format(str(error.retry_after)[:4]), color=ec)
        await ctx.send(embed=embed)
    elif isinstance(error,commands.NotOwner):
        #オーナー専用コマンド
        embed = discord.Embed(title=textto("cmd-error-t",ctx.message.author), description="このコマンドはオーナー専用だってよ", color=ec)
        await ctx.send(embed=embed)
        ch=bot.get_channel(652127085598474242)
        await ch.send(embed=getEmbed("エラーログ",f"コマンド:`{ctx.command.name}`\n```{str(error)}```",ec,f"サーバー",ctx.guild.name,"実行メンバー",ctx.author.name,"メッセージ内容",ctx.message.content))
    elif isinstance(error,commands.MissingRequiredArgument):
        #引数がないよっ☆
        embed = discord.Embed(title=textto("cmd-error-t",ctx.message.author), description=f"値が渡されていない引数があります！\n引数を見直してください！", color=ec)
        await ctx.send(embed=embed)
    else:
        #その他例外
        ch=bot.get_channel(652127085598474242)
        await ch.send(embed=getEmbed("エラーログ",f"コマンド:`{ctx.command.name}`\n```{str(error)}```",ec,f"サーバー",ctx.guild.name,"実行メンバー",ctx.author.name,"メッセージ内容",ctx.message.content))


@bot.command()
async def globalpost(ctx,gmid:int):
    post=None
    cursor.execute("select * from globaldates")
    dats = cursor.fetchall()
    for i in dats:
        if gmid in i["allid"]:
            post = i
    cursor.execute("select * from users where id=?",(ctx.author.id,))
    upf = cursor.fetchone()
    if upf["gmod"]:
        cursor.execute("select * from users where id=?",(i["aid"],))
        u = cursor.fetchone()
        g = bot.get_guild(post["gid"])
        await ctx.send(embed=getEmbed("メッセージ内容",post['content'],ec,"送信者id:",post['aid'],"送信先",post["allid"],"送信者のプロファイルニックネーム",upf['gnick'],"サーバーid",g.id,"サーバーネーム",g.name))
    else:
        cursor.execute("select * from users where id=?",(i["aid"],))
        u = cursor.fetchone()
        g = bot.get_guild(post["gid"])
        await ctx.send(embed=getEmbed("メッセージ内容",post['content'],ec,"送信者id:",post['aid'],"送信者のプロファイルニックネーム",upf['gnick']))

@bot.command()
async def emojiinfo(ctx,*,emj:commands.EmojiConverter=None):

    if emj==None:
        await ctx.send(textto("einfo-needarg",ctx.author))
    elif emj.guild == ctx.guild:
        embed = discord.Embed(title=emj.name, description=f"id:{emj.id}",color=ec)
        embed.add_field(name=textto("einfo-animated",ctx.author), value=emj.animated)
        embed.add_field(name=textto("einfo-manageout",ctx.author), value=emj.managed)
        if emj.user:
            embed.add_field(name=textto("einfo-adduser",ctx.author), value=str(emj.user))
        embed.add_field(name="url", value=emj.url)
        embed.set_footer(text=textto("einfo-addday",ctx.author))
        embed.timestamp = emj.created_at
        await ctx.send(embed=embed)
    else:
        await ctx.send(textto("roleinfo-other",ctx.message.author))

@bot.command()
async def delm(ctx, ctxid):

    if ctx.message.author.permissions_in(ctx.message.channel).manage_messages == True or ctx.author.id == 404243934210949120:
        print(f'{ctx.message.author.name}({ctx.message.guild.name})_'+ ctx.message.content )
        dctx = await ctx.message.channel.fetch_message(ctxid)
        print(f'{ctx.message.author.name}さんのコマンド実行で、{ctx.message.guild.name}でメッセージ"{dctx.content}"が削除されました。')
        await dctx.delete()
        await ctx.message.delete()

@bot.command()
async def dcomrun(ctx,cname,*,ags):
    if ctx.message.author.id == 404243934210949120:
        c = ctx
        c.args = list(ags)
        try:
            await c.invoke(bot.get_command(cname))
        except:
            await ctx.send(embed=discord.Embed(title="dcomrunエラー",description=traceback.format_exc(0)))


@bot.command()
async def mas(ctx,*,text):
    st=""
    for i in text:
        st = st+f"\|\|{i}\|\|"
    await ctx.send(st)

@bot.command()
async def sendlogto(ctx,to=None):
    if ctx.author.guild_permissions.administrator or ctx.author.id == 404243934210949120:
        cursor.execute("select * from guilds where id=?",(ctx.guild.id,))
        gpf = cursor.fetchone()
        if to:
            db.execute("UPDATE guilds SET sendlog = ? WHERE id = ?", (int(to),ctx.guild.id))
            n=ctx.guild.me.nick
            await ctx.guild.me.edit(nick="ニックネーム変更テスト")
            await asyncio.sleep(1)
            await ctx.guild.me.edit(nick=n)
            await asyncio.sleep(1)
            await ctx.send("変更しました。ニックネーム変更通知が送られているかどうか確認してください。")
        else:
            db.execute("UPDATE guilds SET sendlog = ? WHERE id = ?", (None,ctx.guild.id))
            await ctx.send("解除しました。")
    else:
        await ctx.send("このコマンドの使用には、管理者権限が必要です。")

@bot.command()
async def ranklev(ctx):
    cursor.execute("select * from guilds where id=?",(ctx.guild.id,))
    gs = cursor.fetchone()
    async with ctx.channel.typing():
        le = gs["levels"]
        lrs = [(int(k),v["level"],v["exp"]) for k,v in le.items() if v["dlu"]]
        text=""
        for ind,i in enumerate(sorted(lrs, key=itemgetter(1,2), reverse=True)):
            un = ctx.guild.get_member(i[0])
            if un is None:
                un = await bot.fetch_user(i[0])
                if un is None:
                    un=f"id:`{i[0]}`"
                else:
                    un = str(un)+f"({textto('ranklev-outsideg',ctx.author)})"
            else:
                un = un.mention
            if len(text+f"> {ind+1}.{un}\n　level:{i[1]},exp:{i[2]}\n") <= 2036:
                text = text + f"> {ind+1}.{un}\n　level:{i[1]},exp:{i[2]}\n"
            else:
                text = text+f"({textto('ranklev-lenover',ctx.author)})"
                break
        e = discord.Embed(title=textto("ranklev-title",ctx.author),description=text,color=ec)
    await ctx.send(embed=e)

@bot.command()
async def cemojiorole(ctx,name,*rlis):
    ig = await ctx.message.attachments[0].read()
    await ctx.guild.create_custom_emoji(name=name,image=ig,roles=[ctx.guild.get_role(int(i)) for i in rlis])
    await ctx.send(textto("created-text",ctx.author))

@commands.cooldown(1, 10, type=commands.BucketType.guild)
@bot.command()
async def guildlang(ctx,lang):
    cursor.execute("select * from guilds where id=?",(ctx.guild.id,))
    gs = cursor.fetchone()
    print(f'{ctx.message.author.name}({ctx.message.guild.name})_'+ ctx.message.content )
    if textto("language",lang).startswith("Not found language:"):
        await ctx.send(textto("setl-cantuse",ctx.author))
    else:
        cursor.execute("UPDATE guilds SET lang = ? WHERE id = ?", (lang,ctx.guild.id))
        await ctx.send(textto("setl-set",ctx.message.author))

@bot.command()
async def guildprefix(ctx,mode="view",ipf=""):
    cursor.execute("select * from guilds where id=?",(ctx.guild.id,))
    gs = cursor.fetchone()
    if mode=="view":
        await ctx.send(embed=getEmbed("ユーザーのprefix",f'```{",".join(gs["prefix"])}```'))
    elif mode=="set":
        spf = gs["prefix"]+[ipf]
        cursor.execute("UPDATE guilds SET prefix = ? WHERE id = ?", (spf,ctx.guild.id))
        await ctx.send(textto("upf-add",ctx.author).format(ipf))
    elif mode=="del":
        spf = gs["prefix"]
        spf.remove(ipf)
        cursor.execute("UPDATE guilds SET prefix = ? WHERE id = ?", (spf,ctx.guild.id))
        await ctx.send(f"{ipf}を削除しました。")
    else:
        await ctx.send(embed=getEmbed("不適切なモード選択","`view`または`set`または`del`を指定してください。"))
    
@bot.command()
async def cuglobal(ctx,*cids):
    if ctx.message.author.id == 404243934210949120:
        cursor.execute("select * from globalchs")
        chs = cursor.fetchall()
        async with ctx.channel.typing():
            for cid in [int(i) for i in cids]:
                await asyncio.sleep(0.5)
                try:
                    for ch in chs:
                        if cid in ch["ids"]:
                            clt=ch["ids"]
                            clt.remove(cid)
                            db.execute("UPDATE globalchs SET ids = ? WHERE name = ?", (clt,ch["name"]))
                            break
                except:
                    pass
        await ctx.send("強制切断できてるか確認してねー")

@bot.command(name="sina-guild",aliases=["思惟奈ちゃん公式サーバー","思惟奈ちゃんのサーバーに行きたい"])
async def sinaguild(ctx):
    print(f'{ctx.message.author.name}({ctx.message.guild.name})_'+ ctx.message.content )
    await ctx.send("https://discord.gg/udA3qgZ")

@bot.command()
async def test_of_twipost(ctx,text):
    try:
        twi.statuses.update(status=text)
    except:
        await ctx.send(f"```{traceback.format_exc(2)}```")


@tasks.loop(time=datetime.time(hour=23,minute=0,second=0))
async def invite_tweet():
    try:
        twi.statuses.update(status=f"[定期投稿]\nみぃてん☆の公開Discordサーバー:https://discord.gg/GbHq7fz\nみぃてん☆制作、多機能Discordbot思惟奈ちゃん:https://discordapp.com/oauth2/authorize?client_id=462885760043843584&permissions=8&scope=bot\n<この投稿は思惟奈ちゃんより行われました。>")
    except:
        dc=bot.get_user(404243934210949120)
        await dc.send(f"have error:```{traceback.format_exc(1)}```")

@tasks.loop(time=datetime.time(hour=8,minute=0,second=0))
async def now_sina_tweet():
    try:
        twi.statuses.update(status=f"[定期投稿]\n思惟奈ちゃんのいるサーバー数:{len(bot.guilds)}\n思惟奈ちゃんの公式サーバー:https://discord.gg/udA3qgZ\n<この投稿は思惟奈ちゃんより行われました。>")
    except:
        dc=bot.get_user(404243934210949120)
        await dc.send(f"have error:```{traceback.format_exc(1)}```")
    pr=random.choice(partnerg)
    if pr[3]!="":
        e=getEmbed("パートナーサーバー紹介",f"{bot.get_guild(pr[0])}\n{pr[3]}\n参加: {pr[2]}")
        cursor.execute("select * from globalchs where name=?",("main",))
        chs = cursor.fetchone()
        for chid in chs["ids"]:
            try:
                ch = bot.get_channel(chid)
                for wh in await ch.webhooks():
                    try:
                        if wh.name == "sina_global":
                            await wh.send(embed=e)
                            await asyncio.sleep(0.2)
                            break
                    except:
                        continue
            except:
                pass


@bot.command()
async def lrewardupd(ctx):
    async with ctx.channel.typing():
        cursor.execute("select * from guilds where id=?",(ctx.guild.id,))
        gs=cursor.fetchone()
        rslt={}
        for uk,uv in gs["levels"].items():
            u = ctx.guild.get_member(int(uk))
            for k,v in gs["reward"].items():
                if int(k)<=uv["level"]:
                    try:
                        rl = ctx.message.guild.get_role(v)
                        await u.add_roles(rl)
                        if rslt[k]:
                            rslt[k].append(u.display_name)
                        else:
                            rslt[k] = [u.display_name]
                        await asyncio.sleep(0.2)
                    except:
                        pass
    await ctx.send("完了しました。",embed=getEmbed("追加者一覧",f"```{','.join([f'レベル{k}:{v}'] for k,v in rslt.items())}```"))

@bot.command()
async def testA(ctx):
    e=discord.Embed(title="テスト",description="リアクションしてどうぞ",color=ec)
    msg = await ctx.send(embed=e)
    await msg.add_reaction("1️⃣")
    await msg.add_reaction("2️⃣")
    await msg.add_reaction("3️⃣")
    try:
        r, u = await bot.wait_for("reaction_add", check=lambda r,u: r.message.id==msg.id and u.id == ctx.message.author.id,timeout=30)
        if str(r)=="1️⃣":
            e=discord.Embed(title="項目1",description="ブーストするといいことあるよ",color=ec)
        elif str(r)=="2️⃣":
            e=discord.Embed(title="項目2",description="えーっと、書くこと知らないんだってよ",color=ec)
        elif str(r)=="3️⃣":
            e=discord.Embed(title="項目3",description="まあ、これ、あくまで例示だしいいよね？",color=ec)
        else:
            e=discord.Embed(title="項目?",description="このリアクションには、何もないよ！",color=ec)
        await msg.edit(embed=e)
    except asyncio.TimeoutError:
        await msg.edit(embed=discord.Embed(title="タイムアウト！",description="もう一度はじめから試してください。"))

"""@bot.command()
async def cNitro(ctx):
    return 0
    cli=[
        449867036558884866,
        641956259758735360,
        367132890032635904,
        398412979067944961,
        415526420115095554,
        607403193034473491,
        586157827400400907,
        657214718410489869,
        594058726902595596,
        539787492711464960,
        462765491325501445,
        431805523969441803
    ]
    uid=random.choice(cli)
    u=ctx.guild.get_member(uid)
    await ctx.send(f"当選者は||{u.display_name}||さんに決まりました！")"""


@bot.command()
async def backup(ctx,gid:int):
    if not ctx.guild.me.guild_permissions.administrator:
        await ctx.send("このサーバーで、わたしが管理者権限を持ってないので使用できません。")
        return
    try:
        g = bot.get_guild(gid)
        if ctx.author.permissions_in(ctx.channel).administrator == True or ctx.author.id == 404243934210949120:
            pgs=await ctx.send(f"役職\n進行度:0/{len(g.roles)}")
            tk=0
            rlid={}
            async with ctx.channel.typing():
                #役職。rlid(dict)に旧id(str)で参照すれば新idが返ってくる
                for r in g.roles[1:][::-1]:
                    rl=await ctx.guild.create_role(name=r.name,permissions=r.permissions,colour=r.colour,hoist=r.hoist,mentionable=r.mentionable,reason=f"{g.name}より。役職転送コマンド実行による。")
                    await asyncio.sleep(2)
                    rlid[str(r.id)]=rl.id
                    tk=tk+1
                    await pgs.edit(content=f"役職\n進行度:{tk}/{len(g.roles)}")
                await ctx.guild.default_role.edit(permissions=g.default_role.permissions)
                rlid[str(g.default_role.id)]=ctx.guild.default_role.id
                await pgs.edit(content=f"チャンネル\n進行度:0/{len(g.channels)}")
                tk=0
                #チャンネル。
                chlt={}
                for mct,mch in g.by_category():
                    await asyncio.sleep(2)
                    try:
                        ovwt={}
                        await asyncio.sleep(2)
                        for k,v in mct.overwrites.items():
                            try:
                                rl=ctx.guild.get_role(rlid[str(k.id)])
                                ovwt[rl]=v
                            except:
                                pass
                        ct = await ctx.guild.create_category_channel(name=mct.name,overwrites=ovwt)
                        chlt[str(mct.id)]=ct.id
                        tk=tk+1
                        await pgs.edit(content=f"チャンネル\n進行度:{tk}/{len(g.channels)}")
                    except AttributeError:
                        ct = None
                    for c in mch:
                        ovwt={}
                        await asyncio.sleep(2)
                        for k,v in c.overwrites.items():
                            try:
                                rl=ctx.guild.get_role(rlid[k])
                                ovwt[rl]=v
                            except:
                                pass
                        if isinstance(c,discord.TextChannel):
                            cch=await ctx.guild.create_text_channel(name=c.name,category=ct,topic=c.topic,slowmode_delay=c.slowmode_delay,nsfw=c.is_nsfw(),overwrites=ovwt)
                        elif isinstance(c,discord.VoiceChannel):
                            if ctx.guild.bitrate_limit >= c.bitrate:
                                cch=await ctx.guild.create_voice_channel(name=c.name,category=ct,bitrate=c.bitrate,user_limit=c.user_limit,overwrites=ovwt)
                            else:
                                cch=await ctx.guild.create_voice_channel(name=c.name,category=ct,bitrate=ctx.guild.bitrate_limit,user_limit=c.user_limit,overwrites=ovwt)
                        else:
                            pass
                        try:
                            chlt[str(c.id)]=cch.id
                            tk=tk+1
                            await pgs.edit(content=f"チャンネル\n進行度:{tk}/{len(g.channels)}")
                        except:
                            pass
                await pgs.edit(content="チャンネル完了\nnext:絵文字")
                #絵文字
                tk=0
                for e in g.emojis:
                    if len(ctx.guild.emojis)>=ctx.guild.emoji_limit:
                        break
                    print("looping")
                    try:
                        ei = await e.url.read()
                        await ctx.guild.create_custom_emoji(name=e.name,image=ei)
                        await asyncio.sleep(5)
                        print("done")
                    except:
                        await ctx.send(f"```{traceback.format_exc(3)}```")
                await pgs.edit(content="絵文字完了\nnext:ユーザーのban状況")
                #ユーザーのban
                bm = await g.bans()
                tk=0
                for i in bm:
                    await g.ban(user=i.user,reason=i.reason)
                    await asyncio.sleep(2)
                    tk=tk+1
                    await pgs.edit(content=f"ban状況確認\n進行度:{tk}/{len(bm)}")

                await pgs.edit(content="ban状況完了\nnext:サーバー設定")
                #サーバー設定
                icn = await g.icon_url_as(static_format="png").read()
                await ctx.guild.edit(name=g.name,icon=icn,region=g.region,verification_level=g.verification_level,default_notifications=g.default_notifications,explicit_content_filter=g.explicit_content_filter)
                #afk
                if g.afk_channel:
                    await ctx.guild.edit(afk_channel=ctx.guild.get_channel(chlt[str(g.afk_channel.id)]),afk_timeout=g.afk_timeout)
                #システムチャンネル
                if g.system_channel:
                    await ctx.guild.edit(system_channel=ctx.guild.get_channel(chlt[str(g.system_channel.id)]),system_channel_flags=g.system_channel_flags)
                #サーバー招待スプラッシュ
                if str(g.splash_url) and ("INVITE_SPLASH" in ctx.guild.features):
                    sp = await g.splash_url.read()
                    await ctx.guild.edit(splash=sp)
                #サーバーバナー
                if str(g.banner_url) and ("BANNER" in ctx.guild.features):
                    bn = await g.banner_url.read()
                    await ctx.guild.edit(banner=bn)
                await ctx.send("完了しました。")
        else:
            await ctx.send("このサーバーの管理者である必要があります。")
    except:
        await ctx.send(embed=getEmbed("エラー",f"詳細:```{traceback.format_exc(0)}```"))

@bot.command()
async def getby(ctx,k:str):
    await ctx.send(embed=getEmbed("",textto(k,ctx.author)))


@bot.command()
@commands.is_owner()
async def get_ch_id(ctx,cnm:str):
    await ctx.send(embed=getEmbed("一致チャンネル",str([f"{i.name}({i.id})" for i in ctx.guild.channels if i.name==cnm])))

@bot.command()
@commands.is_owner()
async def chlogs(ctx,cid:int,count:int):
    ch = bot.get_channel(cid)
    async for m in ch.history(limit=count):
        await ctx.author.send(embed=getEmbed("メッセージ",m.clean_content,ec,"送信者",str(m.author)))
        await asyncio.sleep(2)

@bot.command()
async def cinvite(ctx,ivt:str):
    i = await bot.fetch_invite(ivt)
    e=discord.Embed(title="サーバー招待の分析",desctiption=f"{str(i.inviter)}による招待",color=ec)
    e.set_author(name=f"{i.guild.name}({i.guild.id})",icon_url=i.guild.icon_url_as(format="png"))
    e.add_field(name="メンバー数",value=f"全{i.approximate_member_count}名\nオンラインメンバー{i.approximate_presence_count}名")
    e.add_field(name="招待チャンネル",value=f"{i.channel.name}({i.channel.type})")
    e.add_field(name="一時リンク?",value=str(i.temporary))
    e.add_field(name="取り消された招待?",value=str(i.revoked))
    e.add_field(name="リンク",value=i.url,inline=False)
    e.set_footer(text="招待の作成日時")
    e.timestamp = i.created_at or discord.Embed.Empty
    await ctx.send(embed=e)

#通常トークン
bot.run(BOT_TOKEN)

#テストトークン
#bot.run(BOT_TEST_TOKEN)
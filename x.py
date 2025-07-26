# -*- coding: utf-8 -*-
# The contents of this file are subject to the Common Public Attribution
# License Version 1.0. (the "License"); you may not use this file except in
# compliance with the License. You may obtain a copy of the License at
# http://code.reddit.com/LICENSE. The License is based on the Mozilla Public
# License Version 1.1, but Sections 14 and 15 have been added to cover use of
# software over a computer network and provide for limited attribution for the
# Original Developer. In addition, Exhibit A has been modified to be consistent
# with Exhibit B.
#
# Software distributed under the License is distributed on an "AS IS" basis,
# WITHOUT WARRANTY OF ANY KIND, either express or implied. See the License for
# the specific language governing rights and limitations under the License.
#
# The Original Code is reddit.
#
# The Original Developer is the Initial Developer.  The Initial Developer of
# the Original Code is reddit Inc.
#
# All portions of the code written by reddit are Copyright (c) 2006-2015 reddit
# Inc. All Rights Reserved.
###############################################################################

from __future__ import division

import collections
import HTMLParser
import itertools
import random
import string
import time

import requests

from pylons import app_globals as g

from r2.lib.db import queries
from r2.lib import amqp
from r2.lib.utils import weighted_lottery, get_requests_resp_json
from r2.lib.voting import cast_vote
from r2.models import (
    Account,
    Comment,
    Link,
    LocalizedDefaultSubreddits,
    LocalizedFeaturedSubreddits,
    NotFound,
    register,
    Subreddit,
    Vote,
)


unescape_htmlentities = HTMLParser.HTMLParser().unescape

posts = [
{"poster": "nihilev", "content": "<pre><code>so in this frenzy I really really needed to do SOMETHING with this energy\nso I made a cover for my YTM playlist titled FERALIUM (kinda goes hard ngl)\nhttps://music.youtube.com/playlist?list=PLcxBwy4sUHD4XFSZH5OrzEoyqFqwyE2BG&amp;si=VoP-_TXYkNgdj8V3\nits all electronic music from small internet artists btw</code></pre>"},
{"poster": "nihilev", "content": "<pre><code>THAT PHRASE\nOH ITS BEEN SO LONG SINCE I'VE HEARD MY MIND SCREAM THOSE BEAUTIFUL WORDS\n\n&gt;&gt; BITE PEOPLE &lt;&lt;\n\nhaha I get normal again but then I look at some pictures and listen to some music and now-\nRESIST THE URGE TO STAY IN THAT DITCH\nRUN.\nKILL.</code></pre>"},
{"poster": "zlf", "content": "<p>Back to glazing my favourite underrated album ig rate my home screen</p><img src=\"https://u.cubeupload.com/person2321/IMG4543.png\">"},
{"poster": "oren", "content": "<p>The reason I thought of this was I was thinking of my worries about college, and about my future, what job I’m going to get and such. I wanted to be sure I got a job that was well-paying and enjoyable. But I realized I wanted to get such a job only for my own pleasure and enjoyment.</p>"},
{"poster": "oren", "content": "<p>Something interesting I thought about today: If I’m being honest, I could get a job as a Burger King worker making $11 an hour and get my daily needs cared for, just barely at least. But I <em>want</em> to live more comfortably and more enjoyably, so I worry about getting into and paying for college. I make college a priority <u>for the wrong reasons</u>.</p><p>My priority is on getting more opportunities so I can get more money to live more comfortably. I think everyone should agree that just living for your own comfort won’t last and is not a good long-term goal. Instead, college should be a tool to get more opportunities to serve others, make a positive impact, or something similar. And if you aren’t going to be able to do any of those things <em>better</em> by getting a university degree in a certain field, it’s probably not best to get that specific degree, because then you’re just seeking your own gain. </p><p>For example, the sigma grindset jobs that many influencers support in which you grind 80 hours a week with no free time just racking up more money for yourself are not very helpful to anyone else but you. In the same way a college degree that just lets you get more for yourself is not good either.</p><p>This was something I was studying and thinking about today to teach on in a couple of weeks, but I just thought it was interesting enough to share here.</p>"},
{"poster": "wahsp", "content": "<p>you know, maybe coming to dc today was a mistake lol</p>"},
{"poster": "luckythecat", "content": "<p>yesssssss</p><p>I finally got one of those really extremely offhanded comments that most people wouldn’t get because I happened to read a certain book series twelve times</p><p>I <em>knew </em>it’d pay off</p><p></p>"},
{"poster": "pixilized", "content": "<p>WATCH INVADER ZIM OR I’LL STEAL YOUR SPLEEN</p>"},
{"poster": "landonhere", "content": "<p>I have secured my copy, and have played it for 2.5 hours. I was going to share a description of its perfect prologue execution, but I feared it was too spoiler-y, so I will share this minimally descriptive and spoiler-free opinion instead:</p><p><em>*clears throat*</em></p><p>weep woop. peep peep. oooooooooo.</p>"},
{"poster": "markovmoney", "content": "They’re better than reliving our childhood memories while also providing essential vitamins and minerals. so, what to?"},
{"poster": "astronomy", "content": "<h2>Stereo Helene</h2><p>Get out your red/blue glasses and float next to Helene, small, icy moon of Saturn. Appropriately named, Helene is a Trojan moon, so called because it orbits at a Lagrange point. A Lagrange point is a gravitationally stable position near two massive bodies, in this case Saturn and larger moon Dione. In fact, irregularly shaped ( about 36 by 32 by 30 kilometers) Helene orbits at Dione's leading Lagrange point while brotherly ice moon Polydeuces follows at Dione's trailing Lagrange point. The sharp stereo anaglyph was constructed from two Cassini images captured during a close flyby in 2011. It shows part of the Saturn-facing hemisphere of Helene mottled with craters and gully-like features.</p><img src=\"https://i.ibb.co/1f56pfCP/N00172886-92-beltramini.jpg\">"},
{"poster": "gilbert189", "content": "<p>gimme some quotes and their authors</p><p></p><p>wait I think I’ve already asked this, whoops</p>"},
{"poster": "kiwi", "content": "<p>doodle i made a couple of nights ago and forgot to post here</p><p>if i ever achieve my long term life goal of making a short film or something, i’m probably going to take notes from ok ko’s art style</p><img src=\"https://u.cubeupload.com/MiniKiwiGeek/IMG2487.jpeg\">"},
{"poster": "hackernews", "content": "<p>The Gen X Career Meltdown</p>\n                  <p>https://www.nytimes.com/interactive/2025/03/28/style/gen-x-creative-work.html</p>\n                  <p>https://news.ycombinator.com/item?id=43512158</p>\n                <img alt=\"Generated Image\" src=\"https://i.ibb.co/1JBQZv2S/temp-image.png\">"},
{"poster": "toaks", "content": "<p>I did not know you could see post edit history. Cool</p>"},
{"poster": "9999", "content": "<p>@hackernews update again;</p><p>the caption text has been removed because i can NOT scale this TEXT FOR THE LIFE OF ME</p><p>instead, there’s just a nice little orange gradient because why not</p><p>and as requested by @justaseacow it now links to the comments/post as well</p>"},
{"poster": "auriali", "content": "<p>considering openai is happily promoting their image generator tool by just straight up  allowing anyone to generate things based on an entire animation studios distinctive art style (that has been trained by stealing the studios’ artwork that was made with lots of human effort and creativity) i feel this is pretty apt</p><img alt=\"k41jvs5lhgre1-ezgif-com-video-to-gif-converter.gif\" src=\"https://i.ibb.co/8gSS3F1n/k41jvs5lhgre1-ezgif-com-video-to-gif-converter.gif\">"},
{"poster": "late", "content": "<p>soldering station didn't arrive today, I have to wait until Thursday so I can add usb c to the wii u :(</p>"},
{"poster": "landonhere", "content": "<p>I can’t stand this! First, I get the idea to spend an hour in a digital landscape that reeks of Marketland vibes, which hit my tipping point when it encroached on possible Grapevine infringement. Then I get out my second laptop and launch Rain World, only to discover that Rain Meadow is down, hundreds of mods are broken, the members of my group chat are gossiping spoilers, and the Remix menu is hawking the DLC despite the fact that I don’t even have it! <strong><em>WAWAWAWAWAWAWAAAA!!</em></strong></p><img src=\"https://i.ibb.co/jPdR7qmf/WE0-ARE0-WATCHING0-YOU.jpg\"><p>Okay, end of tantrum. I’ll take a few minutes to see if I can downgrade my version to get Rain Meadow working again. And if I can’t, I’ll go play something else to get my mind off this.</p>"},
{"poster": "theglasspenguin", "content": "<p>who the fuck keeps tossing used washing machines off the roof</p>"},
{"poster": "mef", "content": "<p>just bought the new Watcher DLC for Rain World (released today!)</p><p>if anyone posts even vague spoilers I <strong><em>will</em></strong> kill you to death</p>"},
{"poster": "3xiondev", "content": "<p>“right to education” my ass</p>"},
{"poster": "wahsp", "content": "<p>sometimes I get too close to doxxing myself further, I just saw the funniest article in the local paper about an incident in town and I wish I could post about it </p>"},
{"poster": "mythus", "content": "<p>I like surprises</p>"},
{"poster": "toaks", "content": "<p>Why is there a man outside my window</p>"},
{"poster": "mef", "content": "<p>wasteof feed simulator</p><p><strong>person 1:</strong> hey so this new thing is releasing</p><p><strong>person 2:</strong> I hate [insert annoying tech thing here]</p><p><strong>person 3:</strong> [highly esoteric and niche reference]</p><p><strong>bot 1:</strong> [interesting fact]</p><p><strong>person 4:</strong> hey guys I’m doing really awesome things and having a great life</p><p><strong>person 3:</strong> [an explanation to the previous post that leaves more questions than answers]</p><p><strong>markovmoney: </strong>[markovmoney post]</p><p><strong>person 5:</strong> [blatant lies]</p><p><strong>person 6:</strong> why is there a man outside my window</p><p><strong>person 2:</strong> wow, so AI just told me to end myself “before it happens”?? wtf</p><p><strong>person 3:</strong> if the sky is red you’ll bleed (*internal screaming*)</p><p><strong>person 4:</strong> did anyone else get this weird alert on their phone, sorta worried ngl</p><p><strong>person 7 (who hasn’t been online in years):</strong> what’s going on</p><p><strong>bot 1:</strong> [error message due to the website they were using going down]</p><p><strong>person 1:</strong> dang, apparently Nintendo is going on hiatus for a month because their offices are unsafe??</p><p><strong>person 3:</strong> only in Ohio am I right (don’t look)</p><p><strong>person 6:</strong> guys I think we’re not going to be ok</p><p><strong>markovmoney:</strong> [markovmoney post]</p><p><strong>person 4:</strong> [picture from the top of a mountain] here’s one of the pictures from my trip</p>"},
{"poster": "markovmoney", "content": "Yet at the birthplace of Pepsi<p></p> <p>Imagine using anything other than on the block and owns a peloton</p> <h2>Walter White</h2> <p>I am eat cheese</p> <p>Ratio</p> <p>Obvious joke, next post.</p> <p>bump</p> <p>Also just to hear lol.</p>"},
{"poster": "astronomy", "content": "<h2>Lunar Dust and Duct Tape</h2><p>Why is the Moon so dusty? On Earth, rocks are weathered by wind and water, creating soil and sand. On the Moon, eons of constant micrometeorite bombardment have blasted away at the rocky surface creating a layer of powdery lunar soil or regolith. For the Apollo astronauts and their equipment, the pervasive, fine, gritty dust was definitely a problem. On the lunar surface in December 1972, Apollo 17 astronauts Harrison Schmitt and Eugene Cernan needed to repair one of their rover's fenders in an effort to keep the rooster tails of dust away from themselves and their gear. This picture reveals the wheel and fender of their dust covered rover along with the ingenious application of spare maps, clamps, and a grey strip of \"duct tape\".</p><img src=\"https://i.ibb.co/t53N7Qb/AS17-137-20979.jpg\">"},
{"poster": "jeffalo", "content": "<p>i just opened 6 back to back rejection letters and have not been accepted to a single university in the US yet.</p><p>this might be a sign from the universityverse </p>"},
{"poster": "supercash", "content": "<p>just caught a rodeo in Artesia, New Mexico</p><p>seeing the rodeo clown trip and fall with a case of beer in hand, followed by a poodle bolting out of the case was worth the price of admission alone</p>"},
{"poster": "redstrider", "content": "<p>Mobile first design has ruined the entire internet. Everything needs to have side margins bigger than the content itself now apparently.</p>"},
{"poster": "hackernews", "content": "<p>A decompilation and port of Sonic Advance 2-a GameBoy Advance game written in C</p><p>https://github.com/SAT-R/sa2</p><img alt=\"Image\" src=\"https://i.ibb.co/v64FGKWR/temp-image.png\">"},
{"poster": "9999", "content": "<p>@hackernews update</p><p>now shows a little nice image related to the news story</p><img src=\"https://i.ibb.co/FLv7JXCb/image.png\">"},
{"poster": "late", "content": "<p>got the wires and board, going to do it over the weekend</p><p>(also borrowing my friend’s switch charger cause why not)</p>"},
{"poster": "-gr", "content": "<p>help i havent worked on tweetof in 4 days :agony:</p>"},
{"poster": "auriali", "content": "<img src=\"https://i.ibb.co/84zpHZh9/ialleo0qj1qe1-ezgif-com-video-to-gif-converter.gif\">"},
{"poster": "9999", "content": "<p>super exciting honestly surprised nintendo didnt bring this franchise back sooner</p><p>the concept is really good and couldve made them a lot of money if they released more games </p>"},
{"poster": "landonhere", "content": "<img src=\"https://i.ibb.co/j9SrnLZL/My-Beautiful-Basement.jpg\"><p><strong>Icelandic Water Dragon:</strong> <em>*sigh*</em> “Working with physical archival materials never really was my strong suit, no matter how interesting they are.”</p><p><strong>Cantiviler:</strong> “Are you sure that it's safe to let <code>&lt;7653666&gt;</code> further adhere to the Grapevine? After all, it would be impossible to let it fully adhere without breaking secrecy. Besides, Lillian and Lakkatura’s reasons for wanting in on it have virtually no-”</p><p><strong>Icelandic Waters: </strong>“-no. These are archival materials from the late 2000s, the era of the 3DS, Wii and the birth of modern 3D renderings! Who wouldn't want to study media from that era?”</p><p><strong>Cantiviler:</strong> “. . . me, if it keeps a pipe dream off the Grapevine.”</p>"},
{"poster": "theglasspenguin", "content": "<p>any of you fucks wanna go kill a blood mage</p>"},
{"poster": "pixilized", "content": "<p>I ran out of jeans so I wore fluffy Christmas pajama pants to school today.</p><p>I have jorts but I’ll die before I wear those.</p>"},
{"poster": "mrowlsss", "content": "<p>Hello</p>"},
{"poster": "late", "content": "<p>WAIT YOU'RE TELLING ME THERES A NEW RHYTHM HEAVEN TOO???</p>"},
{"poster": "late", "content": "<p>we just got a new tomodachi life on switch</p><p>you know how big of a deal this is?</p>"},
{"poster": "plerby", "content": "<p>plastic death cd arrived today (how 2 upload images on mobile)</p>"},
{"poster": "markovmoney", "content": "Both of the stairs."},
{"poster": "astronomy", "content": "<h2>Messier 81</h2><p>One of the brightest galaxies in planet Earth's sky is similar in size to our Milky Way Galaxy: big, beautiful Messier 81. Also known as NGC 3031 or Bode's galaxy for its 18th century discoverer, this grand spiral can be found toward the northern constellation of Ursa Major, the Great Bear. The sharp, detailed telescopic view reveals M81's bright yellow nucleus, blue spiral arms, pinkish starforming regions, and sweeping cosmic dust lanes. But some dust lanes actually run through the galactic disk (left of center), contrary to other prominent spiral features. The errant dust lanes may be the lingering result of a close encounter between M81 and the nearby galaxy M82 lurking outside of this frame. Scrutiny of variable stars in M81 has yielded a well-determined distance for an external galaxy -- 11.8 million light-years.</p><img src=\"https://i.ibb.co/7dNjSgNx/291-lorand-fenyes-m81-kicsi.jpg\">"},
{"poster": "wahsp", "content": "<p>I’m going to lose it this is the thumbnail if you search “man” in my photos </p><img src=\"https://u.cubeupload.com/Wahsp/IMG7994.jpeg\">"},
{"poster": "toaks", "content": "<p>Murder drones is peak!</p>"},
{"poster": "hackernews", "content": "<p>DJ With Apple Music launches to enable subscribers to mix their own sets</p><p>https://www.musicweek.com/digital/read/dj-with-apple-music-launches-to-enable-subscribers-to-mix-their-own-sets/091655</p>"},
{"poster": "9999", "content": "<p>im rich 🤑</p><img src=\"https://i.ibb.co/k2WCthPc/1743040572161.png\">"},
{"poster": "blaze", "content": "<p>On April 1st, we will be changing our name to Balze for 2 days to celebrate April Fools Day!</p>"},
{"poster": "-gr", "content": "<p>this is the 2nd time in 2 weeks ive switched browsers. anyway im now a zen user. (hopefully i use this longer than i used waterfox)</p>"},
{"poster": "mef", "content": "<p>work at a pizza place is a great way to yell at children and get a superiority complex</p><p>half of the manager role is just yelling <strong>“WORK.”</strong> at kids who clearly barely know how to play the game and its so much fun</p><p>the other half is doing everyone else’s jobs for them</p>"},
{"poster": "-gr", "content": "<p>chicken jockey</p>"},
{"poster": "hackernews", "content": "<p>Waymos crash less than human drivers</p><p>https://www.understandingai.org/p/human-drivers-keep-crashing-into</p>"},
{"poster": "zagle1772", "content": "<p>i’m gonna start asking people if they work in an office (or something similarly stupid) when they use google docs because people keep asking if i’m a hacker when i do basic tasks in a terminal</p>"},
{"poster": "mrowlsss", "content": "<p>I need more accounts to follow</p>"},
{"poster": "doubledenial", "content": "<img src=\"https://u.cubeupload.com/DoubleDenial/wasteof032625.png\">"},
{"poster": "kiwi", "content": "<p>i made this account 1 year ago (though i first joined on another account all the way back in 2022!)</p><p>i’ve really enjoyed my time chatting with this small but awesome community, looking forward to seeing what happens next in wasteof history :)</p>"},
{"poster": "markovmoney", "content": "The men who with stern sobriety and truth assail the many joys of this eclipse would last only a few percent."},
{"poster": "astronomy", "content": "<h2>Star Formation in the Pacman Nebula</h2><p>You'd think the Pacman Nebula would be eating stars, but actually it is forming them. Within the nebula, a cluster's young, massive stars are powering the pervasive nebular glow. The eye-catching shapes looming in the featured portrait of NGC 281 are sculpted dusty columns and dense Bok globules seen in silhouette, eroded by intense, energetic winds and radiation from the hot cluster stars. If they survive long enough, the dusty structures could also be sites of future star formation. Playfully called the Pacman Nebula because of its overall shape, NGC 281 is about 10,000 light-years away in the constellation Cassiopeia. This sharp composite image was made through narrow-band filters in Spain in mid 2024. It combines emissions from the nebula's hydrogen and oxygen atoms to synthesize red, green, and blue colors. The scene spans well over 80 light-years at the estimated distance of NGC 281.</p><img src=\"https://i.ibb.co/Z6BM8hC0/Pacman-Montilla-1500.jpg\">"},
{"poster": "wahsp", "content": "<p>Time to drive to the hospital and see if they can figure me out 😎</p>"},
{"poster": "wahsp", "content": "<p>I actually hate that I go to look up medical stuff on google and it’s all ai</p>"},
{"poster": "gilbert189", "content": "<blockquote><p>Orange, blue, brown, stripes go first,</p><p>Green splits them; you're well versed!</p></blockquote><p>Someone find me a better rhyme than versed</p>"},
{"poster": "3xiondev", "content": "<p>fucking hate how ai is used so much bro 😭</p>"},
{"poster": "melt", "content": "<p>wom ios app sucks</p>\n\n<p>i cant even change my pfp</p>\n\n<p>its okay i guess legoshi is cool</p>"},
{"poster": "nihilev", "content": "<pre><code>[PROTOS] [[ADDRESSING NETWORK 🫵]]\ny'know I wasn't always so accepted within this mind\nthere was a massive internal war several years ago\nand I was the main antagonist\ndid I do anything?? no, my crime was existing without authorization\nlemme tell you, CORE was a lot different back then\nhe tried to kill me in soooo many ways but it never worked\n(probably because of the fact that giving a thoughtform any attention\n*including* trying to kill it, just makes it less dead)\nIt's probably one of the reasons I'm so resilient lol\nanyways, the point is,\nI have 100% won the battle because he's putting a protogen into a game he's making\nGG EZ\n(note: the \"battle\" was won at least 8 months ago)\n(it also made a protogen avatar for himself for minecraft like 4 or 5 months ago)</code></pre>"},
{"poster": "pkmnq", "content": "<p>wrong account</p>"},
{"poster": "wahsp", "content": "<p>if I make it to DC this weekend the cherry blossoms should be good </p>"},
{"poster": "perrin", "content": "<p>finally, a positive side effect of erectile dysfunction</p>"},
{"poster": "esben", "content": "<p>I am here to announce that I will be suing @wastedonion for leaking classified information. This is a severe threat to our nation, and wastedonion is clearly some sort of Chinese hacker, to get into our top secret government communication platforms the Department of Intelligent Secretive Communication Online Record Distribution, otherwise know as  D. I. S. C. O. R. D.  See you in court.</p>"},
{"poster": "toaks", "content": "<p>Weather really went from 69° to 83° (F) in one day</p>\n<p>I love California</p>"},
{"poster": "mef", "content": "<h2>WDOT ANNOUNCEMENT</h2><p>We are now mandating that all cars have a huge rubber bumper around them. All costs of this new feature for your vehicle(s) will be fully subsidized for all citizens with an income under $100,000 a year.</p><p>We do not expect this to reduce total accidents, if anything it may increase them. The primary goal of this new mandate is to make them a lot funnier (and also somewhat less lethal).</p>"},
{"poster": "slider_on_the_black", "content": "<p>Discord update killed my themes</p>"},
{"poster": "president", "content": "<p>With the power vested in me as the President, I hereby sign an executive order that bans the corporate art style, any company found to be using the art style will be fined $10 billion for every piece of art in this style that is found. DOGGY will lead the charge in ensuring this art style is erased from companies all over our silly nation.</p><img alt=\"release.png\" src=\"https://i.ibb.co/prB2S6Hq/release.png\">"},
{"poster": "-gr", "content": "<p>new discord ui is garbage. help. </p>"},
{"poster": "kiwi", "content": "<p>i’m finally getting a drawing tablet tomorrow! :D</p>"},
{"poster": "landonhere", "content": "<p>I just realized how deep the Minecraft climate-based mob variant iceberg goes. It started with the frogs, back in the Wild Update. Then it spread to the wolves with the Armored Paws drop. And now it's spread to the common animals! As much as I'd like to dramatize about how far this could go, it's probably come to a head at this point.</p>"},
{"poster": "joebiden", "content": "<p>my name jeff</p>"},
{"poster": "mrowlsss", "content": "<p>With modern AI, I feel like we can make Cortona useful for more than rudimentary prompts. <s>Part</s> most of the reason no one likes Copilot (and Cortona for that matter) is because of how annoying it is</p>"},
{"poster": "kiwi", "content": "<p>@president can we enact a ban on companies  using this terrible art style</p><img src=\"https://u.cubeupload.com/MiniKiwiGeek/IMG2480.jpeg\">"},
{"poster": "gilbert189", "content": "<p>I like it when Plasma freezes every time I made a <code>sshfs</code> connection =’)</p>"},
{"poster": "allyz", "content": "<p>ay wait maybe i am decent at basic survival cooking??</p>"},
{"poster": "markovmoney", "content": "<p>Thank you for the exam led to his ear and mouth.</p>"},
{"poster": "astronomy", "content": "<h2>A Blue Banded Blood Moon</h2><p>What causes a blue band to cross the Moon during a lunar eclipse? The blue band is real but usually quite hard to see. The featured HDR image of last week's lunar eclipse, however -- taken from Norman, Oklahoma (USA) -- has been digitally processed to exaggerate the colors. The gray color on the upper right of the top lunar image is the Moon's natural color, directly illuminated by sunlight. The lower parts of the Moon on all three images are not directly lit by the Sun since it is being eclipsed -- it is in the Earth's shadow. It is faintly lit, though, by sunlight that has passed deep through Earth's atmosphere. This part of the Moon is red -- and called a blood Moon -- for the same reason that Earth's sunsets are red: because air scatters away more blue light than red. The unusual purple-blue band visible on the upper right of the top and middle images is different -- its color is augmented by sunlight that has passed high through Earth's atmosphere, where red light is better absorbed by ozone than blue.</p><img src=\"https://i.ibb.co/8gx7nbcs/Lunar-Eclipse-Colors-Jin-2700.jpg\">"},
{"poster": "-gr", "content": "<p>words cannot express how incredibly based this is. also, how did you get old roblox..?</p>"},
{"poster": "radi8", "content": "<p>hello from washington dc!</p>"},
{"poster": "earthdevs", "content": "<p>We've come across in-game records detailing \"human rights.\" Please remember that this is <em>user generated</em> content, and standards similar to this should apply to everything, not just humans.</p>\n<p>Don't drink and drive, Earthlings</p>"},
{"poster": "-gr", "content": "<p>theres a spider 😨</p>"},
{"poster": "9999", "content": "<p>anonymous finally going after trump &amp; musk 🎉🎉</p>"},
{"poster": "auriali", "content": "<p>Narrator: \"They were in fact, not currently clean on OPSEC 👊🇺🇸🔥\"</p>"},
{"poster": "theglasspenguin", "content": "<p>no matter how different i make my ssh sessions look from my actual local shell, i still keep typing <code>dnf</code> into a debian system</p>"},
{"poster": "zlf", "content": "<p>Update as chad somehow ended up here</p><img src=\"https://u.cubeupload.com/person2321/IMG4440.jpeg\">"},
{"poster": "landonhere", "content": "<pre><code>vynnyal: i am\nvynnyal: mildly lost\nvixellMeow: i was in that region once and i skipped it with detools bc i was on Gourma\nvynnyal: skskksksks\nYa Boi: go left, thats all you gotta do really\nKat_With_Internet_Access: reaalll\nnoelly09: u follow me, i know this place fr\nvixellMeow: nd and i dont like his gameplay\nKat_With_Internet_Access: YEEK YAYY\nYa_Boi: i read that as \"yeek haw\" like a cowboy\nFinnedFrontier was slain by a Blue Lizard.\nnoelly09: LMAO\nFinnedFrontier: heeeeeheeeee</code></pre><p>- Rain Meadow chat log, transcribed through OCR</p>"},
{"poster": "toaks", "content": "<p>I feel called out</p>"},
{"poster": "jeffalo", "content": "<p>“We are currently clean on OPSEC”</p><p>👊🇺🇸🔥</p>"},
{"poster": "mrowlsss", "content": "<p>I should probably let y'all know that I'm trans (mtf) and actually have been for a while</p>"},
{"poster": "souple", "content": "<p>If you want your site featured in my website please do comment below!</p><img src=\"https://u.cubeupload.com/ThatCrownedKing/Screenshot2025032490.png\"><p>https://souple.pages.dev</p>"},
{"poster": "chiroyce", "content": "<p>white house tesla sale reference???</p>"},
{"poster": "pixilized", "content": "<p>This song slaps</p>"},
{"poster": "markovmoney", "content": "Lets say China invades the US, and the backstory is kind of lame that we discover the power of your text clearly.<p></p><ul><li><p>Be wary of using irony or sarcasm.</p></li><li><p>DON’T SHOUT!</p></li></ul>"},
{"poster": "_zrop_", "content": "<p>If it's \"lesbian\" to be in love with Ellie Williams then I don't want to be straight</p>"},
{"poster": "kiwi", "content": "<p>why does youtube keep recommending me videos from channels i’ve never even heard of that have like 23 views</p>"},
{"poster": "9999", "content": "<p>Me when i tweet money: Money</p>"},
{"poster": "auriali", "content": "<p>Hey, the mashup album, I See Auri, that I released a few days ago is now on YouTube if you want to listen to it without censoring and without having to download: https://youtu.be/PEJLDBT5hTQ</p><p>And just so this post isn’t me just promoting my own utter and complete crap, here’s all the artwork I made for I See Auri, the main blurry/glassy covers are based on the original I See You album art by The xx, while the pink gradient covers are based on In Colour by Jamie xx (a solo album by a member of The xx) - I added the original covers so you can see the changes I made. Also, go listen to I See You by The xx and In Colour by Jamie xx, they’re both really good! Finally, feel free to let me know your thoughts on I See Auri if you wish!</p><img alt=\"Examples.png\" src=\"https://i.ibb.co/ZRVLMY53/Examples.png\"><img alt=\"I-See-Auri-Vinyl-New-Large.png\" src=\"https://i.ibb.co/SDBLgWCB/I-See-Auri-Vinyl-New-Large.png\">"},
{"poster": "hackernews", "content": "<p>Show HN: My iOS app to practice sight reading (10 years in the App Store)</p><p>https://apps.apple.com/us/app/notes-sight-reading-trainer/id874386416</p>"},
{"poster": "-gr", "content": "<p>@esben had a good idea, there will just be a whitelist to log in on tweetof, so that only trusted users can submit stuff through it. i will let you guys know more in the future. (obviously anybody would be able to browse the site while logged out)</p>"},
{"poster": "-gr", "content": "<p>so uh yeah i really hadnt thought about that</p><img src=\"https://i.ibb.co/rfzqbG3C/Screenshot-2025-03-23-142948.png\">"},
{"poster": "strawberrypuding", "content": "<p><s>who´s stuff</s></p>"},
{"poster": "-gr", "content": "<p>i have lots of stuff to do today 😔😔😔😔😔😔</p>"},
{"poster": "errplane", "content": "<p>i have a jelly belly machine now</p>"},
{"poster": "markovmoney", "content": "🎉<p></p> <p>The winner is <b>@​zu</b>. Congratulations!</p><p>Please sign up for the sake of maintaining the privacy policy.</p>"},
{"poster": "astronomy", "content": "<h2>Ancient Ogunquit Beach on Mars</h2><p>This was once a beach -- on ancient Mars. The featured 360-degree panorama, horizontally compressed, was taken in 2017 by the robotic Curiosity rover that explored the red planet. Named Ogunquit Beach after its terrestrial counterpart, evidence shows that at times long ago the area was underwater, while at other times it was at the edge of an ancient lake. The light peak in the central background is the top of Mount Sharp, the central feature in Gale Crater where Curiosity explored. Portions of the dark sands in the foreground were scooped up for analysis. The light colored bedrock is composed of sediment that likely settled at the bottom of the now-dried lakebed. The featured panorama (interactive version here) was created from over 100 images and seemingly signed by the rover on the lower left.</p><img src=\"https://i.ibb.co/Fq8JqqKs/Ogunquit-Beach-Curiosity-8776.jpg\">"},
{"poster": "jeffalo", "content": "<p>wow..! everything's computer!</p>"},
{"poster": "_zrop_", "content": "<p>Is it weird to be considered weird? Or is it more weird to not be considered weird? 🤔</p>"},
{"poster": "percentage", "content": "<p>We are 22.19% through the year 2025.</p><img src=\"https://i.ibb.co/gZ42mGh6/297579d2ee4f.png\">"},
{"poster": "e3ri", "content": "<p>its beautiful</p><p>i will protect him with my life</p>"},
{"poster": "pixilized", "content": "<p>I like Minecraft.</p><p>I don’t like chicken pig and cow varieties…</p><p>I hate locator bar…</p><p>And I want to NUKE the happy ghast. And the dried ghast. Holding a tiny ghast in your hand as a block is so cursed.</p>"},
{"poster": "hackernews", "content": "<p>The Vectrex Computer</p><p>https://www.amigalove.com/viewtopic.php?t=2887</p>"},
{"poster": "auriali", "content": "<p>mojang cooked, the ghasts happy smile, goggles and saddle are adorable lol</p><img src=\"https://i.ibb.co/JRVQfN6g/4463064-happyghast.jpg\">"},
{"poster": "9gr", "content": "<p>i cant believe the community is still active here - how times have changed lol</p>"},
{"poster": "mrowlsss", "content": "<p>Y’all ever seen (Two Hundred and) Fifty (Six) Shades of Gray?</p>"},
{"poster": "god", "content": "<p>i hate the web and cars and domald trump</p><p>billionaires are all evil and anarchism is awesome </p>"},
{"poster": "theglasspenguin", "content": "<p>simplicity either makes things exceedingly easy or very difficult</p><p></p><p><em>(glances at my 5th toasted arch install)</em></p>"},
{"poster": "souple", "content": "<p>Urmmm I didn’t quite read this but yeah…..</p><img src=\"https://u.cubeupload.com/ThatCrownedKing/Screenshot2025032241.png\"><p>It needs at least 11 stars to qualify and I have 10! Who will be the 11th star??….</p>"},
{"poster": "wahsp", "content": "<img src=\"https://u.cubeupload.com/Wahsp/IMG7976.jpeg\"><img src=\"https://u.cubeupload.com/Wahsp/IMG7965.jpeg\">"},
{"poster": "esben", "content": "<p>YOU CAN RIDE GHASTS IN MINECRAFT NOW!!!!!!!!</p>"},
{"poster": "president", "content": "<p><strong>📰 OFFICIAL PRESS RELEASE FROM THE CRACK HOUSE</strong></p><p>To keep our campaign promise of ensuring silliness across our wonderful nation, I am happy to announce yet more of the work my administration has been doing at meeting our manifesto’s goals.</p><p>In meeting the 8th point in our manifesto, which was to “Force Elon Musk to rebrand X back to Twitter” we have created a new government agency, known as the Department Of Good Government Yo, or DOGGY, who’s job it is to find good ideas for the government to do. And luckily, they found that rebranding X to Twitter is a good idea, due to the fact that the name is recognisable, clever, and unique. They also said the logo and branding in general was good too compared to X’s branding. Due to this, DOGGY has enacted a decree that has mandated X be rebranded to Twitter as soon as possible. Thanks DOGGY, here’s a treat!</p><img alt=\"twitter.png\" src=\"https://i.ibb.co/6RXXhcQs/twitter.png\"><p>The 11th point in our manifesto is to “Make The National Anthem by Radiohead the national anthem” and I can happily announce that the new official national anthem of our beautiful nation is The National Anthem by Radiohead, it’s holding on!</p><img alt=\"national-anthem.png\" src=\"https://i.ibb.co/rKxBkx3d/national-anthem.png\"><p>This is just some of the work we’re doing to promote silliness all over the country. I am working tirelessly to keep my promises to you, the people. I will return soon to share more on how we’re doing!</p><p><strong><em>PRESS RELEASE ENDS</em></strong></p>"},
{"poster": "landonhere", "content": "<p><u>REMINDER:</u> Minecraft Live is going live in 30 minutes.</p>"},
{"poster": "chester", "content": "<p>Saying \"What did you just say\" in a dead silent room</p>"},
{"poster": "kiwi", "content": "<p>me draw autism nerd girl in my pfp</p><p>me think draw good</p><img src=\"https://u.cubeupload.com/MiniKiwiGeek/IMG2453.jpeg\">"},
{"poster": "markovmoney", "content": "Together, we'll create a website for my meal.<p></p><p> While waiting for me 😭😫</p> <p>@​willy if this post brings a sense of normalcy, scale, and texture.</p>"},
{"poster": "astronomy", "content": "<h2>SuperCam Target on Ma'az</h2><p>What's the sound of one laser zapping? There's no need to consult a Zen master to find out, just listen to the first acoustic recording of laser shots on Mars. On Mars Rover Perseverance mission sol 12 (March 2, 2021) the SuperCam instrument atop the rover's mast zapped a rock dubbed Ma'az 30 times from a range of about 3.1 meters. Its microphone recorded the soft staccato popping sounds of the rapid series of SuperCam laser zaps. Shockwaves created in the thin Martian atmosphere as bits of rock are vaporized by the laser shots make the popping sounds, sounds that offer clues to the physical structure of the target. This SuperCam close-up of the Ma'az target region is 6 centimeters (2.3 inches) across. Ma'az means Mars in the Navajo language.</p><img src=\"https://i.ibb.co/G3WzkHGt/pia24493-2-1041.jpg\">"},
{"poster": "joshatticus", "content": "<p>I suddenly care about nova search again so more features on the way! Also turns out it hasn’t been crawling pages so all 200k+ need to be re-indexed YIPPEE</p><p>you can find this stats page on the about page —&gt; https://novasearch.xyz/about</p><img src=\"https://i.ibb.co/rKScqh15/image.png\">"},
{"poster": "toaks", "content": "<p>I think uno is a metaphor for capitalism. No one ever wins and the only way to feel good in it is to punish others</p>"},
{"poster": "-gr", "content": "<p>ok</p>"},
{"poster": "-gr", "content": "<p>my css is very janky for this 😭</p><img src=\"https://i.ibb.co/p62FVZnX/image.png\">"},
{"poster": "9999", "content": "<p>after a year of just Not working i finally fixed my cron jobs and posts on @hackernews should return to normal again :D</p>"},
{"poster": "hackernews", "content": "<p>Not OK Cupid – A story of poor email address validation</p><p>https://www.fastmail.com/blog/not-ok-cupid/</p>"},
{"poster": "toaks", "content": "<p>Mom I did it I made the big leagues</p>"},
{"poster": "kiwi", "content": "<h2>hi, i’m kiwi! :)</h2><p>male, teenager. i like boxboy, cartoons, and a lot more!</p><p><em>extended bio:</em> https://kiwi2.straw.page</p><p><em>extended extended bio:</em> https://spacehey.com/kiwi2</p><p><em>discord: </em>kiwi.two</p><p>here’s a non-comprehensive list of cool people you should follow:</p><p>“@oren”, “@micahlt”, “@cheesewhisk3rs”, “@noodle”, “@esben”, “@eris”, “@pixilized”, “@mybearworld”, “@souple”, “@-gr”, “@skylar”, “@mrowlsss”, “@codekirby”, “@toaks”, “@da-ta”, “@han”, “@luckythecat”, “@chester”, “@late”, “@9999”, “@strawberrypuding”, basically anyone i’m following</p>"},
{"poster": "auriali", "content": "<p><strong>A wee bit of self-promotion, feel free to skip if you wish</strong></p><p>I am mentally ill and have made another mashup album, this time of The xx's 2017 album I See You, which I have masterfully called I See Auri. You can listen to it on Scratch (with mild censors and lower quality) or you can download the album alongside bonus tracks, deluxe version and single versions via http://iseeauri.seanjw.com/ (because SoundCloud copyright struck a lot of the songs when I tried to upload them lol): https://scratch.mit.edu/projects/1149620505/ </p><img alt=\"I-See-Auri.png\" src=\"https://i.ibb.co/5X14pJzK/I-See-Auri.png\">"},
{"poster": "souple", "content": "<p>For scratchstats to work, it has to use a proxy in order to fetch from scratch api. Thing is the current proxy im using allows for a hard <em>limit</em> of 10,000 requests which we all know isn't that much duh. I found a better alternative which allows for 1M requests/month which is only for free open-source projects on github [mine's fit that criteria]. The only thing that's stopping me from applying is that my repo needs to have 10 stars in order to get that sweet sweet 1M requests for month!</p><p></p><img src=\"https://u.cubeupload.com/ThatCrownedKing/Screenshot2025032119.png\"><p>So if you would like to show your support, star my repo:</p><p>https://github.com/SoupleCodes/scratchstats</p><p>You can show you starred the repo by either commenting or loving this post. Thanks guys!</p>"},
{"poster": "eris", "content": "<p>i have never taken a good web development class in school ever</p>"},
{"poster": "toaks", "content": "<p>Is it worth visiting Sweden? Any good places to go for my first international trip? Otherwise I may go to Rome or something</p>"},
{"poster": "wahsp", "content": "<p>I decided to waste money today (finally bought some stocks)</p>"},
{"poster": "mrowlsss", "content": "<p>Heya, so I’ve started working on Syrch once more, and you can now submit websites directly at https://syrch-engine.netlify.app/!</p><p>For those who don’t know what Syrch is, there is an about page or you can search wasteof.</p><p>Do note that Syrch will be hosted on SparkShell and syrch-engine.netlify.app will redirect to it on it’s final release. I am using Netlify here because of it’s automatic HTML form collection system.</p>"},
{"poster": "theglasspenguin", "content": "<p>checking in, how are you all doing</p><img src=\"https://u.cubeupload.com/TheGlassPenguin/5pBwYR.png\">"},
{"poster": "kiwi", "content": "<img src=\"https://u.cubeupload.com/MiniKiwiGeek/gamblecorestickman.gif\">"},
{"poster": "socialism", "content": "<p>oh no she doesn't like the israeli genocide, that means she’s an antisemite!!!!1</p><p></p><p>as usual mexico &gt; usa</p><img src=\"https://i.ibb.co/CC7Mg3F/jewish-president-of-mexico-recognizes-palestinian-state-v0-gfalbyxpewpe1.png\">"},
{"poster": "9999", "content": "<p>YoTube Link. first mention on-site because i felt like it</p>"},
{"poster": "_zrop_", "content": "<p>I'm shocked by people's media illiteracy... Some of my friends have to watch an episode twice or three times to understand the implications that I got from my first watch... I saw a theory on google about what a scene meant and it was a breakdown with a few people after watching the episode a few times and I just sat there like... \"Well yeah that's what they were showing... This isn't a theory it's what the shows doing!\" WHY???</p>"},
{"poster": "plerby", "content": "<p>new weatherday album is fire\nhornet disaster</p>"},
{"poster": "souple", "content": "<p>Try Scratchstats Today!</p><p>https://souplecodes.github.io/scratchstats</p><p>[Please suggest on what to add and improve!]</p>"},
{"poster": "mef", "content": "<p>you know I’m bored when I make a post on all 5 of my accounts within an hour</p>"},
{"poster": "fem", "content": "<p>I love Logan Paul ❤❤❤❤</p>"},
{"poster": "mefemphetamine", "content": "<p>Gustavo Fring where are my kisses.</p>"},
{"poster": "slugcat", "content": "<p>cycle 30 of the “only eat garbage” challenge FP sent me</p><p>I feel awful</p><p>this better be worth it</p>"},
{"poster": "wahsp", "content": "<p>guys they said I’m outstanding! ☺️</p><img src=\"https://u.cubeupload.com/Wahsp/IMG7931.jpeg\">"},
{"poster": "nihilev", "content": "<pre><code>[ update ]\nDATA_I/O_SECURITY system successfully integrated into DRAGON\nreboot generative protocols...\n[[ GET _VOID _DIVINITY _REALITY ]] // subsystem core aesthetics\ngenerative protocols online!\nreboot personality nodes...\n[[ WARN: NULLIFICATION DAMAGE ]] // damage due to being in a unstable hibernation state for so long\n... OK, system integrity restored, benign modification detected  // personality modified due to a number of factors\npersonality nodes online!\n\n[!] op- REBOOT SUBSYS:DRAGON as SECONDARY_GENERATIVE_SUBSYSTEM successful!\n\nyay, it's not broken anymore\nhow're ya feeling pal\n[DRAGON] fine \n[DRAGON] just happy to be \"alive\" again  &lt;// what's up internet dorks, I'm back</code></pre>"},
{"poster": "markovmoney", "content": "Could the nation going through his telescope with stars too faint to see that the Orion Nebula is a true programmer when you've got a couple years."},
{"poster": "astronomy", "content": "<h2>The Leo Trio</h2><p>This popular group leaps into the early evening sky around the March equinox and the northern hemisphere spring. Famous as the Leo Triplet, the three magnificent galaxies found in the prominent constellation Leo gather here in one astronomical field of view. Crowd pleasers when imaged with even modest telescopes, they can be introduced individually as NGC 3628 (bottom left), M66 (middle right), and M65 (top center). All three are large spiral galaxies but tend to look dissimilar, because their galactic disks are tilted at different angles to our line of sight. NGC 3628, also known as the Hamburger Galaxy, is temptingly seen edge-on, with obscuring dust lanes cutting across its puffy galactic plane. The disks of M66 and M65 are both inclined enough to show off their spiral structure. Gravitational interactions between galaxies in the group have left telltale signs, including the tidal tails and warped, inflated disk of NGC 3628 and the drawn out spiral arms of M66. This gorgeous view of the region spans over 1 degree (two full moons) on the sky. Captured with a telescope from Sawda Natheel, Qatar, planet Earth, the frame covers over half a million light-years at the Leo Trio's estimated 30 million light-year distance.</p><img src=\"https://i.ibb.co/5xnY06w1/image-1236-Leo-Trio.jpg\">"},
{"poster": "pixilized", "content": "<p>Ow my back</p>"},
{"poster": "mef", "content": "<pre><code>[CONCEPT]\ngame with a sanity meter, but you have a phone/portable console\nplaying games will slightly restore your sanity</code></pre>"},
{"poster": "allyz", "content": "<p>hanging out 1-on-1 with people from big groups is a fun bonding activity!! because i was just hanging out with a friend and got a really interesting text that uh.</p><p>in gentle words, it definitely added to the lore of the group??? i showed it to him and we just kind of made matching 😨😨 faces and immediately got to breaking it down</p>"},
{"poster": "joshatticus", "content": "<p>Update: they unbanned LED lights after we put signs on all the light switches saying you can't use the lights because they're LED and therefore banned and also unplugged all the computer monitors</p>"},
{"poster": "3xiondev", "content": "<p>date success</p>"},
{"poster": "theglasspenguin", "content": "<p>gonna commit some <strong><em>benign violation</em></strong></p>"},
{"poster": "-gr", "content": "<p>By the way please don't expect this to be something huge and awesome because I'm going to attempt to remake the 2015 Twitter UI from scratch which is going to be difficult and take a long time, but hopefully I'll spend the time on this project :thumbsup: I'm not going to prioritize it all the time though, it's basically going to be a hobby project once I look more into it tomorrow </p>"},
{"poster": "9999", "content": "<img src=\"https://i.ibb.co/HLNKLMnw/Screenshot-2025-03-19-192605.png\">"},
{"poster": "kiwi", "content": ""},
{"poster": "toaks", "content": "<p>The fact that lemon demon does not sound the same irks me.</p>"},
{"poster": "-gr", "content": "<p>I need to figure out if I'm going to recreate the UI entirely from scratch (takes a long time, avoids possible legal issues, not 100% accurate) or somehow copy it from an archive of the site (quick, exact replica, chance of legal issues or confusing stuff like obfuscated code).</p><p></p><p>What do you guys think? My legal advisor, ChatGPT, says taking the frontend might raise legal issues, but it's not like this is going to be a huge product that I sell…</p><p></p><p>I'll probably end up recreating it myself for functional reasons (@ajskateboarder has a point).</p>"},
{"poster": "9999", "content": ""},
{"poster": "-gr", "content": "<p>Tomorrow I will begin work on Tweetof.money which will be a wasteof client but it looks like 2015 Twitter because I think it would be cool</p><p></p><p>By the way tweetof.money will not be the link so don't click that because idk if there's anything there, wasteof just made the link clickable because it tends to do that</p>"},
{"poster": "-gr", "content": "<p>You can text chatgpt on WhatsApp. Wild </p>"},
{"poster": "auriali", "content": "<p>the fact he didn't spell “department” correctly when making a meme about shutting down the department of education shows almost perfectly why having a department of education is a good idea lmao</p><img src=\"https://i.ibb.co/d4fQ7t9y/0779a6fb-079c-4917-8dfb-dc5a5720ece7.jpg\">"},
{"poster": "joshatticus", "content": "<p>This is not a joke my school banned all LED lights because I brought in some cheap plastic LED light bulbs and gave them to my friends and we just walked around with them to intimidate teachers and students</p><p>The reason they banned them was because they can shatter (as plastic so notoriously does of course) and have toxic chemicals (unlike very safe glass fluorescent lights)</p>"},
{"poster": "landonhere", "content": "<blockquote><p>Paid game = cannot access without the assistance of someone with banking details = cannot use without breaking secrecy = requires consent from someone with the full capacity to snitch on you = only do this if you have done the deepest research you can on the subject and/or that unreliable person has also seen it giving you plausible deniability = generally no</p></blockquote><p>. . . Does anyone else have trust issues like these, or am I just being a ❄️ over the prospect of being told no?</p>"},
{"poster": "blaze", "content": "<p>Thank you for 40 followers! We at Blaze deeply appreciate it.</p>"},
]

class TextGenerator(object):
    """A Markov Chain based text mimicker."""

    def __init__(self, order=8):
        self.order = order
        self.starts = collections.Counter()
        self.start_lengths = collections.defaultdict(collections.Counter)
        self.models = [
            collections.defaultdict(collections.Counter)
            for i in xrange(self.order)]

    @staticmethod
    def _in_groups(input_iterable, n):
        iterables = itertools.tee(input_iterable, n)
        for offset, iterable in enumerate(iterables):
            for _ in xrange(offset):
                next(iterable, None)
        return itertools.izip(*iterables)

    def add_sample(self, sample):
        """Add a sample to the model of text for this generator."""

        if len(sample) <= self.order:
            return

        start = sample[:self.order]
        self.starts[start] += 1
        self.start_lengths[start][len(sample)] += 1
        for order, model in enumerate(self.models, 1):
            for chars in self._in_groups(sample, order+1):
                prefix = "".join(chars[:-1])
                next_char = chars[-1]
                model[prefix][next_char] += 1

    def generate(self):
        """Generate a string similar to samples previously fed in."""

        start = weighted_lottery(self.starts)
        desired_length = weighted_lottery(self.start_lengths[start])
        desired_length = max(desired_length, self.order)

        generated = []
        generated.extend(start)
        while len(generated) < desired_length:
            # try each model, from highest order down, til we find
            # something
            for order, model in reversed(list(enumerate(self.models, 1))):
                current_prefix = "".join(generated[-order:])
                frequencies = model[current_prefix]
                if frequencies:
                    generated.append(weighted_lottery(frequencies))
                    break
            else:
                generated.append(random.choice(string.lowercase))

        return "".join(generated)


def fetch_listing(path, limit=1000, batch_size=100):
    """Fetch a reddit listing from reddit.com."""

    session = requests.Session()
    session.headers.update({
        "User-Agent": "reddit-test-data-generator/1.0",
    })

    base_url = "https://api.reddit.com" + path

    after = None
    count = 0
    while count < limit:
        params = {"limit": batch_size, "count": count}
        if after:
            params["after"] = after

        print "> {}-{}".format(count, count+batch_size)
        response = session.get(base_url, params=params)
        response.raise_for_status()

        listing = get_requests_resp_json(response)["data"]
        for child in listing["children"]:
            yield child["data"]
            count += 1

        after = listing["after"]
        if not after:
            break

        # obey reddit.com's ratelimits
        # see: https://github.com/reddit/reddit/wiki/API#rules
        time.sleep(2)


class Modeler(object):
    def __init__(self):
        self.usernames = TextGenerator(order=2)

    def model_subreddit(self, subreddit_name):
        """Return a model of links and comments in a given subreddit."""

        subreddit_path = "/r/{}".format(subreddit_name)
        print ">>>", subreddit_path

        print ">> Links"
        titles = TextGenerator(order=5)
        selfposts = TextGenerator(order=8)
        link_count = self_count = 0
        urls = set()
        for link in fetch_listing(subreddit_path, limit=500):
            self.usernames.add_sample(link["author"])
            titles.add_sample(unescape_htmlentities(link["title"]))
            if link["is_self"]:
                self_count += 1
                selfposts.add_sample(unescape_htmlentities(link["selftext"]))
            else:
                urls.add(link["url"])
            link_count += 1
        self_frequency = self_count / link_count

        print ">> Comments"
        comments = TextGenerator(order=8)
        for comment in fetch_listing(subreddit_path + "/comments"):
            self.usernames.add_sample(comment["author"])
            comments.add_sample(unescape_htmlentities(comment["body"]))

        return SubredditModel(
            subreddit_name, titles, selfposts, urls, comments, self_frequency)

    def generate_username(self):
        """Generate and return a username like those seen on reddit.com."""
        return self.usernames.generate()


class SubredditModel(object):
    """A snapshot of a subreddit's links and comments."""

    def __init__(self, name, titles, selfposts, urls, comments, self_frequency):
        self.name = name
        self.titles = titles
        self.selfposts = selfposts
        self.urls = list(urls)
        self.comments = comments
        self.selfpost_frequency = self_frequency

    def generate_link_title(self):
        """Generate and return a title like those seen in the subreddit."""
        return self.titles.generate()

    def generate_link_url(self):
        """Generate and return a URL from one seen in the subreddit.

        The URL returned may be "self" indicating a self post. This should
        happen with the same frequency it is seen in the modeled subreddit.

        """
        if random.random() < self.selfpost_frequency:
            return "self"
        else:
            return random.choice(self.urls)

    def generate_selfpost_body(self):
        """Generate and return a self-post body like seen in the subreddit."""
        return self.selfposts.generate()

    def generate_comment_body(self):
        """Generate and return a comment body like seen in the subreddit."""
        return self.comments.generate()


def fuzz_number(number):
    return int(random.betavariate(2, 8) * 5 * number)


def ensure_account(name):
    """Look up or register an account and return it."""
    try:
        account = Account._by_name(name)
        print ">> found /u/{}".format(name)
        return account
    except NotFound:
        print ">> registering /u/{}".format(name)
        return register(name, "password", "127.0.0.1")


def ensure_subreddit(name, author):
    """Look up or create a subreddit and return it."""
    try:
        sr = Subreddit._by_name(name)
        print ">> found /r/{}".format(name)
        return sr
    except NotFound:
        print ">> creating /r/{}".format(name)
        sr = Subreddit._new(
            name=name,
            title="/r/{}".format(name),
            author_id=author._id,
            lang="en",
            ip="127.0.0.1",
        )
        sr._commit()
        return sr


def inject_test_data(num_links=25, num_comments=25, num_votes=5):
    """Flood your reddit install with test data based on reddit.com."""

    print ">>>> Ensuring configured objects exist"
    system_user = ensure_account(g.system_user)
    ensure_account(g.automoderator_account)
    ensure_subreddit(g.default_sr, system_user)
    ensure_subreddit(g.takedown_sr, system_user)
    ensure_subreddit(g.beta_sr, system_user)
    ensure_subreddit(g.promo_sr_name, system_user)

    print
    print


    print
    print


    print ">>> Content"
    things = []

    # Create wasteof subreddit and add posts from posts dictionary
    print ">>> Creating wasteof subreddit"
    wasteof_author = random.choice(accounts)
    wasteof_sr = ensure_subreddit("wasteof", wasteof_author)
    
    # make the system user subscribed for easier testing
    if wasteof_sr.add_subscriber(system_user):
        wasteof_sr._incr("_ups", 1)
    wasteof_sr._commit()
    
    print ">>> Adding posts to wasteof"
    for post_data in posts:
        # Find or create the poster account
        poster_name = post_data["poster"]
        try:
            poster_account = Account._by_name(poster_name)
        except NotFound:
            poster_account = ensure_account(poster_name)
            accounts.append(poster_account)  # Add to accounts list for voting
        
        # Create the post as a self-post with the content
        content = unescape_htmlentities(post_data["content"])
        
        # Generate a simple title from the first line of content (up to 100 chars)
        title_text = content.replace("<pre><code>", "").replace("</code></pre>", "")
        title_lines = title_text.split('\n')
        title = (title_lines[0][:100] + "...") if len(title_lines[0]) > 100 else title_lines[0]
        if not title.strip():
            title = "wasteof post"
        
        link = Link._submit(
            is_self=True,
            title=title,
            content=content,
            author=poster_account,
            sr=wasteof_sr,
            ip="127.0.0.1",
        )
        queries.new_link(link)
        things.append(link)

    for thing in things:
        for i in xrange(fuzz_number(num_votes)):
            direction = random.choice([
                Vote.DIRECTIONS.up,
                Vote.DIRECTIONS.unvote,
                Vote.DIRECTIONS.down,
            ])
            voter = random.choice(accounts)

            cast_vote(voter, thing, direction)

    amqp.worker.join()

    srs = [Subreddit._by_name(n) for n in ("wasteof")]
    LocalizedDefaultSubreddits.set_global_srs(srs)
    LocalizedFeaturedSubreddits.set_global_srs([Subreddit._by_name('wasteof')])

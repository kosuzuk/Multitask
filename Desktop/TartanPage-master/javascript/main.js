/*jslint browser: true*/
/*global $, jQuery, alert*/
var newDate, curMin, curHour, month, curDay, year;
var bgIndex = -1;
var bgMax = 7;
var funFact = "Carnegie Mellon's original campus architect is said to have modeled his design after a ship. The prow of the historic USS Pennsylvania rests atop Roberts Hall, which overlooks Panther Hollow and the Carnegie Museum complex. \n\
In December 1955, professor Herbert Simon and business Ph.D. student Allen Newell made a breakthrough that would place them among the founders of artificial intelligence — inventing a programming language for computers to model complex human problem-solving processes.\n\
The flat grassy area in the middle of campus known as \"the Cut\" was originally a huge ravine, deeper than the tennis courts area. Over the years, it was filled in with dirt removed when the school cut down a 43-foot hill for the College of Fine Arts building and a 56-foot hill to provide access to Forbes Avenue at Morewood. \n\
Drama majors, or \"dramats,\" signed their names on the walls of the Green Room behind the main stage of Carnegie Mellon's Kresge Theatre. Among these young hopefuls: Ted Danson, Blair Underwood, Laura San Giacomo, Judith Light and Steven Bochco. \n\
Carnegie Mellon's Tepper School of Business is home to the \"Management Game,\" an exercise in teamwork and group dynamics, that was modeled after Procter & Gamble and the soap industry. Created here in the 1950s, it was the first simulation program of its kind offered at a business school. Today, it is widely copied by other top business schools. \n\
In the early 1980s, researchers at Carnegie Mellon's Field Robotics Center created robotic machines that cleaned up nuclear waste at Three Mile Island. Years later, other prototypes were used in the Chernobyl accident clean-up in Ukraine. \n\
Carnegie Mellon’s popularity spills over to the silver and small screens. The university has been endorsed by characters on \"Buffy the Vampire Slayer\" and \"The West Wing,\" spoofed by \"The Muppets\" (Dr. Bunsen Honeydew went to Carnegie Melonhead University), and scenes from the movies \"Smart People,\" \"The Mothman Prophecies,\" \"Wonder Boys,\" \"Dogma,\" and \"Flashdance\" were filmed on campus.\n\
\"The Fence\" was erected in 1923 so seniors could sit and watch the world go by. Three administrations were unable to remove it. Today, it is a passionately guarded billboard for both sanctioned and unsanctioned announcements, as well as editorial comments on campus life.\n\
In the early 1940s, the silicone rubber in Silly Putty was discovered by a Dow Corning employee working on a research fellowship at Mellon Institute. Earl Warrick was working with silicone compounds and came up with the strange, pliable material that stretches, bounces and absorbs printed impressions.\n\
\"Buggy\" began in 1920 as the \"Sweepstakes Race\" and highlights the Spring Carnival each year. Drivers squeeze themselves into the student-designed vehicles and steer as they're pushed over a mile-long course by competing teams from fraternities, sororities and other student organizations.\n\
Carnegie Mellon worked with IBM in the 1980s to develop Andrew — a pioneering computer network that links the entire campus through thousands of personal computers and work stations. In 2000, Carnegie Mellon continued its technical tradition with a campus-wide wireless network. Today, Carnegie Mellon consistently ranks as one of the \"most wired\" campuses in America.\n\
School of Computer Science research professor Scott Fahlman has long been credited for introducing emoticons (also called smileys) while posting to an online bulletin board in 1981. An emoticon is a series of ordinary printable characters, such as :-) , ;o) or :-(, intended to represent a human facial expression and convey an emotion.\n\
During World War I, 16 temporary buildings were built on the then Carnegie Institute of Technology campus to serve as barracks, training facilities and mess halls for soldiers in training for technical, engineering and mechanical war work.   By 1918, 8,000 soldiers and sailors were living on campus.\n\
In 2002, Universal Pictures released \"A Beautiful Mind,\" an Academy award-winning film directed by Ron Howard about Carnegie Mellon alumnus John Nash Jr. and his 30-year battle with schizophrenia. Nash earned his bachelor's and master's degrees in mathematics in 1948 and won the Nobel Prize in Economic Science in 1994.\n\
In 1949, the only male member of Carnegie Institute of Technology's \"Modern Dance Club\" was a young man named Andrew Warhola. Decades later, Andy Warhol became known as a pop art icon.\n\
"

function main() {
    'use strict';

    var userName = localStorage.getItem("userName");
    var greeting = ["Greetings, ", "How are you, ", "Welcome, ", 
                    "Heart in the work? ", "Change the world, "];
    var greetIndex = Math.floor((Math.random() * 10) + 1) % 5;
    
    if (userName !== null) {
        $('#startPage').hide();
        $('#userName').text(userName + "!");
        $('#hello').text(greeting[greetIndex]);
    }


    $('textarea').bind("enterKey",function(e){
        userName = $('textarea').val();
        $('#startPage').fadeOut(350);
        $('body').fadeIn(350);

        if(typeof(Storage) !== "undefined") {
            localStorage.setItem("userName", userName);
        }

        $('#userName').text(userName);

    });

    $('textarea').keydown(function(e){
        if(e.keyCode === 13)
        {
            e.preventDefault();
            return false;
        }
    });

    $('textarea').keyup(function(e){
        if(e.keyCode === 13)
        {
            e.preventDefault();
            $(this).trigger("enterKey");

        }
    });

    updateClock()
}






    /********************************************/
    /**********    Digital Clock      ***********/
    /*******************************************/



function updateClock() {
    var months = ["January", "February", "March", "April", "May",
                  "June", "July", "August", "September", "October",
                  "November", "December"]
    var iths = ["st", "nd", "rd", "th"]


    function ithsX(i) {
        if (i == 1 || i == 21 || i == 31) {
            return iths[0];
        }else if (i == 2 || i == 22) {
            return iths[1];
        }else if (i == 3 || i == 23) {
            return iths[2];
        }else {
            return iths[3];
        }
    }

    function doubleDigit(i) {
        if (i < 10) {
            return "0" + i;
        } else {
            return i;
        }
    }

    function updateClock() {
        newDate = new Date();

        curSec = newDate.getSeconds();
        curMin = newDate.getMinutes();
        curHour = newDate.getHours();
        month = newDate.getMonth();
        curDay = newDate.getDay();
        year = newDate.getFullYear();


        $('#time').text(doubleDigit(curHour) + ":" + doubleDigit(curMin) + ":" + doubleDigit(curSec));
        $('#date').text(months[month] + " " + curDay + ithsX(curDay) + ", " + year);

    }
    var timer = setInterval(function () {
        updateClock();
    }, 1000);

    var diningTimer = setInterval(function () {
        updateDiningOptions();
    }, 60000);

    updateDiningOptions();

    
    var busTimer = setInterval(function () {
        getBustime();
    }, 60000); 
    
    var bgTimer = setInterval(updateBg, 12000);

    updateDiningOptions();
    updateClock();
    getBustime();
    putOnWeather();
    updateBg();

}




    /********************************************/
    /**********    Dining Services   ***********/
    /*******************************************/

function showFunFact() {
    var listOfFunFact = funFact.split(/\n/);
    document.getElementById("funfact").innerHTML = listOfFunFact[Math.round(Math.random()*listOfFunFact.length)]
}



function getDay() {
return curDay;
}

function getTime() {
    return {
        hour: curHour,
        min: curMin
    }
}

function updateDiningOptions(){
    var diningInfo = [];
    $.ajax({
        url: 'http://apis.scottylabs.org/dining/v1/locations',
        success: function(json) {
            var day = getDay();
            var time = getTime();
            function timeDiff(t1, t2) {
                var time = {
                    hour: t1.hour - t2.hour,
                    min: t1.min - t2.min
                };
                if (time.min < 0) {
                    time.hour--;
                    time.min += 60;
                }
                return time;
            }
            function toMin(t) {
                return t.hour*60 + t.min;
            }

            for (var index in json.locations) {

                var place = json.locations[index];
                var opTime = null;
                for (var index in place.times) {
                    if (place.times[index].start.day == day) {
                        opTime = place.times[index];
                    }
                }
                if (opTime === null) {
                    message = "Closed Today";
                    rank = 5;
                } else {
                    var startDiff = timeDiff(time, opTime.start);
                    var endDiff = timeDiff(time, opTime.end);
                    var startDiffMin = toMin(startDiff);
                    var endDiffMin = toMin(endDiff);

                    function formatMin(x) {
                        if (x == 0) return "00";
                            else return ""+x;
                    }

                    var message, rank;

                    if (opTime.start.hour < opTime.end.hour) {
                        if (-60 <= startDiffMin && startDiffMin < 0) {
                            message = "Opening in" + Math.abs(startDiffMin) + "min"
                            rank = 1;
                        } else if (-60 <= endDiffMin && endDiffMin < 0) {
                            message = "Closing in" + Math.abs(endDiffMin) + "min";
                            rank = 2;
                        } else if (startDiffMin < -60) {
                            message = "Opening at " + opTime.start.hour + ":" + formatMin(opTime.start.min);
                            rank = 3;
                        } else if (endDiffMin >= 0 || startDiffMin < 0) {
                            message = "Closed"
                            rank = 4;
                        } else {
                            message = "Open";
                            rank = 0;
                        }
                    } else {
                        if (-60 <= startDiffMin && startDiffMin < 0) {
                            message = "Opening in" + Math.abs(startDiffMin) + "min"
                            rank = 1;
                        } else if (-60 <= endDiffMin && endDiffMin < 0) {
                            message = "Closing in" + Math.abs(endDiffMin) + "min";
                            rank = 2;
                        } else if (endDiffMin > 0 && startDiffMin < -60) {
                            message = "Opening at" + opTime.start.hour + ":" + formatMin(opTime.start.min);
                            rank = 3;
                        } else if (endDiffMin > 0 && startDiffMin < 0) {
                            message = "Closed"
                            rank = 4;
                        } else {
                            message = "Open";
                            rank = 0;
                        }
                    }
                }
                diningInfo.push({
                    name: place.name,
                    message: message,
                    rank: rank
                })

            }
            putOnDiningOption(diningInfo);
        }
    })
}


function putOnDiningOption(diningInfo) {
    var container = document.getElementById('diningContainer');
    // Remove old dom elements
    while (container.firstChild) {
        container.removeChild(container.firstChild);
    }
    var ul = document.createElement('ul');
    ul.setAttribute('class', 'diningOptions');

    container.appendChild(ul);
    diningInfo.sort(function(x, y) {
        return x.rank - y.rank;
    })
    diningInfo.forEach(renderDiningList);

    function renderDiningList(ele, ind, arr) {
        var li = document.createElement('li');
        li.setAttribute('class', 'rank'+ele.rank);

        var name = document.createElement('div');
        name.setAttribute('class', 'place');
        name.innerHTML = ele.name;
        var time = document.createElement('div');
        time.setAttribute('class', 'message');
        time.innerHTML = ele.message;
        li.appendChild(name);
        li.appendChild(time);

        ul.appendChild(li);
    }

}


    /********************************************/
    /**********      Bus Services    ***********/
    /*******************************************/

function getBustime() {

	$.ajax({
		url: 'http://cors-anywhere.herokuapp.com/truetime.portauthority.org/bustime/wireless/html/eta.jsp?route=---&direction=---&displaydirection=---&stop=---&id=4407',
        type: 'GET',
		success: function(text) {
			var busRegex = /<b>#(.*)&nbsp;/g;
			var busNumers = [];
			var busTimes = [];
			while (busStr = busRegex.exec(text)) {
				busNumers.push(busStr[1]);
			}


			var busTimeRegex = /<b>(DUE|.*MIN)<\/b>/g;
			while (busStr = busTimeRegex.exec(text)) {
				busTimes.push(busStr[1].replace("&nbsp;", "").replace("DUE", "NOW"));
			}

			busInfo = [];
			for (var i = 0; i < busNumers.length; i++) {
				busInfo.push({
					name: busNumers[i],
					time: busTimes[i]
				})
			}
			putOnBustime(busInfo);
		}
	})
}

function putOnBustime(busInfo) {

	var container = document.getElementById('busContainer');


    // Remove old dom elements
    while (container.firstChild) {
        container.removeChild(container.firstChild);
    }
	var ul = document.createElement('ul');
	ul.setAttribute('id', 'morewood');
	ul.setAttribute('class', 'busStop');

	container.appendChild(ul);
	busInfo.forEach(renderBusList);

    if (busInfo.length === 0) {
        var li = document.createElement('li');
        li.innerHTML = "No Available Buses";
        ul.appendChild(li);
    }

	function renderBusList(ele, ind, arr) {
		var li = document.createElement('li');
		var name = document.createElement('div');
		name.setAttribute('class', 'bus');
		name.innerHTML = ele.name;
		var time = document.createElement('div');
		time.setAttribute('class', 'time');
		time.innerHTML = ele.time;
		li.appendChild(name);
		li.appendChild(time);

		ul.appendChild(li);
	}

}


   /********************************************/
    /*******        Background       ***********/
    /*******************************************/

function updateBg() {
    if (bgIndex < 0) {
        bgIndex = bgIndex + 1;
    } else {
        bgIndex = bgIndex + 1;
        if (bgIndex > bgMax || bgIndex == bgMax) {
            bgIndex = 0;
        }
        $('.background').fadeOut(600, function() {
            $('.background').attr('src', 'images/background/'+ bgIndex +'.gif');
            $('.background').fadeIn(600);
        });
    }
    
} 


   /********************************************/
    /**********        Weather       ***********/
    /*******************************************/






function putOnWeather() {
    $.ajax({
        url: "http://api.wunderground.com/api/1205bbca123028ac/forecast/q/PA/Pittsburgh.json",
        success: function(data) {
            //Each list represents a day. Each sublist represents weather code, hi, lo, and cur temp(for today).
            var lst = []
            for (var i = 1; i < 4; i++) {
                var x = data.forecast.simpleforecast.forecastday[i]
                lst.push({
                    weekday: x.date.weekday_short,
                    weather: x.conditions, 
                    hi: x.high.fahrenheit + "°F", 
                    lo: x.low.fahrenheit + "°F", 
                    iconURL: x.icon_url
                })
            }
            return getHourly(lst)
        }
    })
}

function getHourly(lst) {
    $.ajax({
        url: "http://api.wunderground.com/api/1205bbca123028ac/hourly/q/PA/Pittsburgh.json",
        success: function(data) {
            //Each list represents an hour. Each sublist represents weather code, temp.
            var hLst = []
            for (var i = 0; i < 24; i++) {
                var x = data.hourly_forecast[i];
                hLst.push({
                    weather: x.condition,
                    temp: x.temp.english + "°F",
                    hour: x.FCTTIME.hour,
                    iconURL: x.icon_url
                })
                
           }
           return updatingWeather(lst, hLst)
        }
    })
}


var weatherIconPair =
[["Drizzle", "rain"],
["Rain", "rain"],
["Snow", "snow"],
["SnowGrains", "snow"],
["IceCrystals", "snow"],
["IcePellets", "snow"],
["Hail", "snow"],
["Mist", "rain"],
["Fog", "cloudy"],
["FogPatches", "cloudy"],
["Smoke", "cloudy"],
["VolcanicAsh", "cloudy"],
["WidespreadDust", "cloudy"],
["Sand", "cloudy"],
["Haze", "cloudy"],
["Spray", "rain"],
["DustWhirls", "cloudy"],
["Sandstorm", "cloudy"],
["LowDriftingSnow", "snow"],
["LowDriftingWidespreadDust", "cloudy"],
["LowDriftingSand", "cloudy"],
["BlowingSnow", "snow"],
["BlowingWidespreadDust", "cloudy"],
["BlowingSand", "cloudy"],
["RainMist", "rain"],
["RainShowers", "rain"],
["SnowShowers", "snow"],
["SnowBlowingSnowMist", "snow"],
["IcePelletShowers", "snow"],
["HailShowers", "rain"],
["SmallHailShowers", "rain"],
["Thunderstorm", "rain"],
["ThunderstormsandRain", "rain"],
["ThunderstormsandSnow", "snow"],
["ThunderstormsandIcePellets", "rain"],
["ThunderstormswithHail", "rain"],
["ThunderstormswithSmallHail", "rain"],
["FreezingDrizzle", "rain"],
["FreezingRain", "rain"],
["FreezingFog", "cloudy"],
["PatchesofFog", "cloudy"],
["ShallowFog", "cloudy"],
["PartialFog", "cloudy"],
["Overcast", "sunnycloudy"],
["Clear", "sunnydaytime"],
["PartlyCloudy", "cloudy"],
["MostlyCloudy", "cloudy"],
["ScatteredClouds", "sunnycloudy"],
["SmallHail", "rain"],
["Squalls", "cloudy"],
["FunnelCloud", "cloudy"]]


function updatingWeather(lst, hLst) {

    var currenttemp = document.getElementById('currenttemp');
    currenttemp.innerHTML = hLst[0].temp;
    currenttemp.setAttribute('style', 'margin-left: 150px; \
                            font-Family :Avenir, Geneva, sans-serif;\
                            margin-top: -25px; ')
    currenttemp.style.fontSize = '400%';
    currenttemp.style.color = "white";
    var weatherBigIcon = document.getElementById('weathericon');
    


    var bigImg = document.createElement('img');
    bigImg.setAttribute('width', '70px');
    bigImg.setAttribute('style', 'margin-left: 50px;\
                                    margin-top: -25px');

    if (getTime.hour > 19) {
        bigImg.setAttribute("src", "./weathericonswhite/nighttime.svg");
    } else {
        for (var i = 0; i < weatherIconPair.length; i++) {
            if ((hLst[0].weather.replace(" ", "")).indexOf(weatherIconPair[i][0]) != -1) {
                var iconPair = weatherIconPair[i];
                break;
            }
        }
        bigImg.setAttribute("src", "./weathericonswhite/"+iconPair[1]+".svg");
    }
    weatherBigIcon.appendChild(bigImg);


    var dailyContainer = document.getElementById('dailyContainer');
    var ulDaily = document.createElement('ul');

    dailyContainer.appendChild(ulDaily);
    lst.forEach(renderDailyList);

    function renderDailyList(ele, ind, arr) {

        var li = document.createElement('li');
        var weekday = document.createElement('div');
        weekday.innerHTML = ele.weekday;

        // var weather = document.createElement('div');
        // weather.innerHTML = ele.weather;

        var lo = document.createElement('div');
        lo.innerHTML = ele.lo;

        var hi = document.createElement('div');
        hi.innerHTML = ele.hi;

        var iconCont = document.createElement('div');
        var icon = document.createElement( 'img' );
        icon.setAttribute('src', ele.iconURL);
        iconCont.appendChild(icon);

        li.appendChild(weekday);
        // li.appendChild(weather);
        li.appendChild(lo);
        li.appendChild(hi);
        li.appendChild(iconCont);
        ulDaily.appendChild(li);
    }

    var hourlyContainer = document.getElementById('hourlyContainer');
    var ulHourly = document.createElement('ul');
    hourlyContainer.appendChild(ulHourly);
    hLst.forEach(renderHourlyList);

    function renderHourlyList(ele, ind, arr) {
        var li = document.createElement('li');

        var hour = document.createElement('div');
        hour.innerHTML = ele.hour + ":00";

        // var weather = document.createElement('div');
        // weather.innerHTML = ele.weather;

        var temp = document.createElement('div');
        temp.innerHTML = ele.temp;

        var icon = document.createElement('img');
        icon.setAttribute('src', ele.iconURL);

        li.appendChild(hour);
        // li.appendChild(weather);
        li.appendChild(temp);
        li.appendChild(icon);

        ulHourly.appendChild(li);
    }
}





$(document).ready(main);

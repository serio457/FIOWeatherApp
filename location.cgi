#!/usr/local/rvm/rubies/ruby-2.2.1/bin/ruby
# FILE: test.cgi
# Francesco Serio, 2019
# 
# 	Test file for ~testing~

# require any libraries that are used
require 'cgi'
require 'net/http'
require 'json'
require 'date'
cgi = CGI.new ("html5")

# print out errors to the webpage for easier debugging and syntax error correction
$stdout.sync = true
$stderr.reopen $stdout

city = cgi['city']

# convertDate takes in the date portion of the hash, converts it into a ruby 
# date format, and then converts that into a user-friendly string 
def convertDate(date)
     dateHash = date
     dateFormat = Date.parse dateHash
     dateString = dateFormat.strftime('%A, %b %d')
     return dateString     
end

# convertCity takes in the city portion of the hash and splits them on a space, 
# then it capitalizes each word and joins them back together so the name of every
# city will be a proper noun
def convertCity(city)
     (city.split(" ").collect do |word| 
         word.capitalize 
     end).join(" ")
end

city = convertCity(city) #store what's converted by convertCity in the variable city in order for it to be able to be used in the second part of the Net::HTTP.get

forecastLocation = String.new("/v1/forecast.json?key=7e3e22f0e430441e99e161226191007&q=" + city.delete(' ')+ "," + cgi['state'] + "&days=6") # uses NET::HTTP.get to access the API   
foo = Net::HTTP.get('api.apixu.com', forecastLocation) # store the whole hash for the forecast JSON call
bar = JSON.parse(foo) # parses a JSON string, constructing the JavaScript value or object described by the string
fugazi = bar['forecast'] # 

currentLocation = String.new("/v1/current.json?key=7e3e22f0e430441e99e161226191007&q=" + city.delete(' ')+ "," + cgi['state'])# uses NET::HTTP.get to access the API
foo2 = Net::HTTP.get('api.apixu.com', currentLocation) # 
bar2 = JSON.parse(foo2) # parses a JSON string, constructing the JavaScript value or object described by the string
fugazi2 = bar2['current'] #


puts "Content-type: text/html\r\n\r"
puts '<!DOCTYPE html>'
puts '<html lang="en">'

puts '<head>'
puts '    <meta charset="UTF-8">'
puts '    <meta name="viewport" content="width=device-width, initial-scale=1.0">'
puts '    <meta http-equiv="X-UA-Compatible" content="ie=edge">'
puts '  <link rel="stylesheet" href="style.css" />'
puts '  <title>Weather for ' + city + ', ' + cgi['state'] + '</title>'
puts '</head>'
     puts '<body>'
     	puts '<div>'
		puts '<h1> The weather in ' + city + ', ' + cgi['state'] + ' is </h1>'
		puts '<table class = "egt">'
                        puts '<tr>'
                                puts '<th>Current Temp (F)</th>'
                                puts '<th>	Feels Like (F)</th>'
                                puts '<th>	Predicted High (F)</th>'
                                puts '<th>	Predicted Low (F)</th>'
                                puts '<th>	Description</th>'
				puts '<th>	Icon</th>'
                        puts '</tr>'

			puts '<tr>'
			        puts "<td>" + fugazi2['temp_f'].to_s + "</td>"
                        	puts "<td>" + fugazi2['feelslike_f'].to_s + "</td>"
				puts "<td>" + fugazi['forecastday'][0]['day']['maxtemp_f'].to_s + "</td>"
				puts "<td>" + fugazi['forecastday'][0]['day']['mintemp_f'].to_s + "</td>"
				puts "<td>" + fugazi2['condition']['text'].to_s + "</td>"
				puts "<td>" + "<img src='http:" + fugazi2['condition']['icon'] + "'></td>"
			puts '</tr>'
                puts '</table>'
        puts '</div>'
     	
     	puts '<div>'
     		puts '<h2> 5 Day Forecast </h2>'
      		
		puts '<table class = "egt">'
			puts '<tr>'
				puts '<th>Day</th>'
				puts '<th>Predicted High (F)</th>'
				puts '<th>Predicted Low (F)</th>'
				puts '<th>Description</th>'
				puts '<th>Neato Icon</th>'	
			puts '</tr>' 
			
			# for the 6 days taken in, skipping the first since we just want the next five days, put the day, max, min temps, and description and icon in a table
			fugazi['forecastday'].drop(1).each do |item| 
				date = item['date']
				dateString = convertDate(date)   	   
     				
				puts '<tr>' 
					puts '<td>' + dateString + '</td>'
					puts "<td>" + item['day']['maxtemp_f'].to_s + "</td>"
					puts "<td>" + item['day']['mintemp_f'].to_s + "</td>"
					puts "<td>" + item['day']['condition']['text'].to_s + "</td>"
   					puts "<td>" + "<img src = 'http:" + item['day']['condition']['icon'] + "'></td>"
				puts '</tr>'
			end

			puts '</table>'
	puts '</div>'	
    	
	puts 'Click <a href="http://www.cs.transy.edu/fserio/WEATHER">here</a> to search for weather in another location!'

     puts '</body>'
puts '</html>'



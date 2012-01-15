#!/usr/bin/env ruby
nas_directories = ["Z:\\TV A-H\\", "Z:\\TV I-R\\", "Z:\\TV S-Z\\"]
local_dir = "G:\\DL\\"
shows = {}
# Track all the series that are located on the NAS
nas_directories.each(){ |dir|
  Dir.entries(dir).each(){ |nas_show|
    if nas_show != ".." && nas_show != "."
      shows[nas_show] = dir + nas_show
    end
  }
}
puts shows

pattern = /S\d{1,2}E\d{1,2}/
not_pattern = /[^(S\d{1,2})&&[^(E\d{1,2})]]+/
commands = []

# Loop through directories/files in local dir
Dir.entries(local_dir).each() { |file|
  #puts file
	if file.index(pattern) != nil
		#puts file
		# The name matches a possible tv show, check if the show is in the shows array
		# First get the name of the series from filename
		filename = file.slice(0, file.index(pattern)).strip
		#puts filename
		if shows.has_key?(filename)
		    # Copy file to remote dir
			mkdircmd = ("mkdir \""+shows[filename]+"/"+file+"/\"").gsub("/","\\")
			copycmd = ("copy \""+local_dir+file+"\" \""+shows[filename]+"/"+file+"/\"").gsub("/","\\")
			delcmd = ("rmdir \""+local_dir+file+"\" /S /Q")
			puts mkdircmd
			puts copycmd
			puts delcmd
			puts "Add above commands to queue? Enter to approve, \"s\" to skip, \"k\" to keep (no delete)"
			input = gets.strip
			if input == "s"
				
			elsif input == "k"
				commands += [mkdircmd, copycmd]
			else
				commands += [mkdircmd, copycmd, delcmd]
			end
		    #system(mkdircmd)
		    #system(copycmd)
		end
		#puts "blap"
	end
}

print "------------------------------------"

commands.each() { |cmd|
	system(cmd)
}

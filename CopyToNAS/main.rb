nas_directories = ["Z:/TV A-H/", "Z:/TV I-R/", "Z:/TV S-Z/"]
local_dir = "D:/DL/"
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

# Loop through directories/files in local dir
Dir.entries(local_dir).each() { |file|
  #puts file
  if file.index(pattern) != nil
    puts file
    # The name matches a possible tv show, check if the show is in the shows array
    # First get the name of the series from filename
    filename = file[not_pattern].strip
    puts filename
    if shows.has_key?(filename)
      # Copy file to remote dir
      mkdircmd = "mkdir "+ "\""+shows[filename]+"/"+file+"/\"".gsub("/","\\")
      copycmd = "copy \""+local_dir+file+"\" \""+shows[filename]+"/"+file+"/\"".gsub("/","\\")
      puts mkdircmd
      puts copycmd
      system(mkdircmd)
      system(copycmd)
    end
    #puts "blap"
  end
}
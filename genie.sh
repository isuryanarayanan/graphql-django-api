#!/usr/bin/env bash

# This script is the gateway to start developing with the project.
# It will start the docker containers and load the environment variables according to the
# configuration you want to work in.

# -----------
# How to use:
# -----------
# 1. Run the script
# 2. Select the configuration you want to work in
# 3. The script will start the docker containers and load the environment variables
# 4. You can now start developing

# -----------
# How to add a new configuration:
# -----------
# 1. Run the command using --create flag
# 2. Give a name to the configuration
# 3. Give a description to the configuration
# 4. The script will create a new configuration file in .genie/configurations folder
# 5. Change your configuration file according to your needs
# 6. Run the script and select your new configuration

# -----------
# How to build a configuration:
# -----------
# 1. Run the command using --build flag
# 2. Select the configuration you want to build
# 3. The script will build the configuration
# -----------

# Check if necessary folders are available
if [ ! -d ".genie/configurations" ]; then
    mkdir .genie/configurations
fi

if [ ! -d "conf" ]; then
    mkdir conf
fi

# Flags
create=false
help=false
build=false

# Parsing flags
while [[ $# -gt 0 ]]
do
key="$1"

case $key in
    -c|--create)
    create=true
    shift # past argument
    ;;
    -h|--help)
    help=true
    shift # past argument
    ;;
    -b|--build)
    build=true
    shift # past argument
    ;;
    *)    # unknown option
    shift # past argument
    ;;
esac
done

# If help flag is set, show help
if [ "$help" = true ]; then
    echo "Usage: genie.sh [options]"
    echo "Options:"
    echo "  -c, --create     Create a new configuration"
    echo "  -h, --help       Show this help"
    exit
fi

# If create flag is set, create a new configuration
if [ "$create" = true ]; then
    echo "----------------------------"
    echo "Creating a new configuration"
    echo "----------------------------"
    read -p "Enter name: " name
    read -p "Enter description: " description
    read -p "Enter keyword: " keyword
    echo "Creating configuration $name ..."
    echo "{
    \"name\": \"$name\",
    \"description\": \"$description\",
    \"keyword\": \"$keyword\",
    \"binded\": false
}" > .genie/configurations/$keyword.json
    echo "Configuration file created"
    exit
fi


# Checking FZF installation
if [ $(dpkg-query -W -f='${Status}' fzf 2>/dev/null | grep -c "ok installed") -eq 0 ];
then
	# Requesting root

	SUDO=''
	if (( $EUID != 0 )); then
			echo "Please run as root"
			SUDO='sudo'
			exit
	fi
	$SUDO apt-get install fzf;
fi

# Checking jq installation
if [ $(dpkg-query -W -f='${Status}' jq 2>/dev/null | grep -c "ok installed") -eq 0 ];
then
    # Requesting root

    SUDO=''
    if (( $EUID != 0 )); then
            echo "Please run as root"
            SUDO='sudo'
            exit
    fi
    $SUDO apt-get install jq;
fi


# For each mode inside .genie/configurations folder, fzf will show a list of options which is the name of the mode.
# Fzf will also show the mode description as preview.
selected_mode=$(ls .genie/configurations | fzf --prompt "Search configuration > " --preview "cat .genie/configurations/{} | jq '.description'")

# If no mode is selected, exit
if [ -z "$selected_mode" ]; then
    echo "No configuration selected"
    exit
fi

# Load the configuration file
configuration=$(cat .genie/configurations/$selected_mode)

# Check if the configuration is binded
binded=$(echo $configuration | jq '.binded')
# Get the keyword of the configuration
keyword=$(echo $configuration | jq '.keyword')
# Remove quotes from the keyword
keyword=$(echo $keyword | sed 's/"//g')



if [ "$binded" = false ]; then

    # Binding a configuration means the necessary files for container defenition will be created using the base files
    # and the configuration file will be updated to binded=true

    echo "Binding configuration $selected_mode ..."
    
    # If not created create a folder with the name keyword inside the conf folder
    if [ ! -d "conf/$keyword" ]; then
        mkdir conf/$keyword
    fi

    # Copy the base files to the keyword folder
    cp .genie/docker/docker-compose.yml conf/$keyword/docker-compose.yml
    cp .genie/docker/Dockerfile conf/$keyword/Dockerfile
    cp .genie/docker/.env conf/$keyword/.env

    # Update the docker-compose file to switch the __keyword__ with the keyword
    echo $configuration | jq '.keyword' | sed 's/"//g' | xargs -I {} sed -i "s/__keyword__/{}/g" conf/$keyword/docker-compose.yml

    # Update the configuration file to binded=true
    echo $configuration | jq '.binded = true' > .genie/configurations/$selected_mode
    # show loading for 2 seconds
    sleep 2
    echo "Configuration $selected_mode binded"
fi


# Run the docker-compose file
# Only build if the build flag is set
if [ "$build" = true ]; then
    docker compose -f conf/$keyword/docker-compose.yml build
fi

docker compose -f conf/$keyword/docker-compose.yml run --service-ports 'project-'$keyword bash

# Ask if the user wants to close the session
read -p "Do you want to close your session? [y/n] " close_session

if [ "$close_session" != "y" ]; then
    echo "Succesfully exited without closing your session."
    exit
fi

docker compose -f conf/$keyword/docker-compose.yml down
echo "Succesfully closed your session."
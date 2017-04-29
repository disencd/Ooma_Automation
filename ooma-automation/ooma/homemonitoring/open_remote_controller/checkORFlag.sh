#!/bin/sh
#
# checkORFlag
#

OR_VER_FILE=/var/run/openremote.ver
OR_CURRENT_LINK=/ipkg/openremote_current
OR_BIN_RELPATH=OpenRemote-Controller/bin

MDM_FILE=/opt/etc/ooma/mdm.cfg
OR_RESOURCES_DIR=/opt/openremote_resources
OR_WEBAPPS_SECURITY_USERS="$OR_RESOURCES_DIR/users.xml"
OR_CONFIG_RULES_DIR="$OR_RESOURCES_DIR/rules"

EVENT_PROCESSOR_CONFIG_FILE_DIR="$OR_RESOURCES_DIR/ooma"
EVENT_PROCESSOR_CONFIG_FILE="$EVENT_PROCESSOR_CONFIG_FILE_DIR/eventProcessor-config.xml"
BEEHIVE_CONFIG_FILES_DIR="$OR_RESOURCES_DIR"
BEEHIVE_CONFIG_USER_FILE="$BEEHIVE_CONFIG_FILES_DIR/.user"
BEEHIVE_CONFIG_PASSWORD_FILE="$BEEHIVE_CONFIG_FILES_DIR/.password"

HMS_ENABLED_PARAM_NAME='HMS_ENABLED'
HMS_USER_ENABLED_PARAM_NAME='HMS_USER_ENABLED'
HMS_NIMBITS_EMAIL_PARAM_NAME='HMS_NIMBITS_EMAIL'
HMS_NIMBITS_TOKEN_PARAM_NAME='HMS_NIMBITS_TOKEN'
HMS_NIMBITS_URL_PARAM_NAME='HMS_NIMBITS_URL'
HMS_BEEHIVE_USER_PARAM_NAME='HMS_BEEHIVE_USER'
HMS_BEEHIVE_PASSWORD_PARAM_NAME='HMS_BEEHIVE_PASSWORD'
HMS_BEEHIVE_URL_PARAM_NAME='HMS_BEEHIVE_URL'
HMS_LOG_LEVEL_PARAM_NAME='HMS_LOG_LEVEL'
HMS_CONTROLLER_ID_PARAM_NAME='HMS_CONTROLLER_ID'

currentDate() { echo -n $(date +"%Y-%m-%d %T%z") ; }
#debug() { echo "$(currentDate) $@"; }
debug() { echo "$(currentDate) $@" >> /tmp/checkorflag.log ; echo "$(currentDate) $@"; }

# param=$1; mdm_file=$2
# return value of param line in $file containing "^$param"
# there should not be multiple keys in the file
get_mdm_param() {
    local mdm_file=${2:-$MDM_FILE}
    if [ ! -r $mdm_file ] ; then return 1 ; fi
    if [ -z $1 ] ; then return 1 ; fi
    local value=$(grep -m 1 "^$1" $mdm_file | cut -d = -f 2)
    echo -n "$value"       # strip linefeed

}

get_hms_enabled() { echo -n $(get_mdm_param ${HMS_ENABLED_PARAM_NAME}) ; }
get_hms_user_enabled() { echo -n $(get_mdm_param ${HMS_USER_ENABLED_PARAM_NAME}) ; }

get_hms_nimbits_email() { echo -n $(get_mdm_param ${HMS_NIMBITS_EMAIL_PARAM_NAME}) ; }
get_hms_nimbits_token() { echo -n $(get_mdm_param ${HMS_NIMBITS_TOKEN_PARAM_NAME}) ; }
get_hms_nimbits_url() { echo -n $(get_mdm_param ${HMS_NIMBITS_URL_PARAM_NAME}) ; }
get_hms_beehive_user() { echo -n $(get_mdm_param ${HMS_BEEHIVE_USER_PARAM_NAME}) ; }
get_hms_beehive_password() { echo -n $(get_mdm_param ${HMS_BEEHIVE_PASSWORD_PARAM_NAME}) ; }
get_hms_beehive_url() { echo -n $(get_mdm_param ${HMS_BEEHIVE_URL_PARAM_NAME}) ; }
get_hms_log_level() { echo -n $(get_mdm_param ${HMS_LOG_LEVEL_PARAM_NAME}) ; }
get_hms_controller_id() { echo -n $(get_mdm_param ${HMS_CONTROLLER_ID_PARAM_NAME}) ; }

openremote_is_running() { ps |grep siege|grep -vq grep ;  }

# get running version of openremote
get_openremote_running_ver() {
    local or_ver_file=${1:-$OR_VER_FILE}
    if ! openremote_is_running; then
        if [ -r $or_ver_file ]; then 
            rm -rf $or_ver_file;
        fi
        echo -n ""
        return
    fi

    if ! [ -r $or_ver_file ]; then
        echo -n ""
        return
    fi
    cat $or_ver_file
}

# get current(target) version of openremote
get_openremote_current_ver() {
    local or_current_link=${1:-$OR_CURRENT_LINK}
    if ! [ -h $or_current_link ]; then
        echo -n ""
        return
    fi
    local ver=0
    local ver=$(ls -l $or_current_link | sed "s/.*-\\([0-9]*\\)\\..*/\\1/;t;c$ver")
    echo -n $ver
}

stop_running_openremote() {
    if [ -f $OR_VER_FILE ]; then rm -f $OR_VER_FILE; fi
    debug "Stop runnning openremote"
    killall -9 siege &> /dev/null
}

start_current_openremote() {
    debug "Start openremote_current"
    local controller_id=${1:-1}
    local beehive_url=$2
    local log_level=$3
    source /etc/profile
    local saved_pwd=$(pwd)
    local or_base_path="$(readlink $OR_CURRENT_LINK)/"
    local or_bin_path="$(readlink $OR_CURRENT_LINK)/$OR_BIN_RELPATH"
    cd $or_bin_path
    debug "openremote --id $controller_id --path $or_base_path &> /var/tmp/openremote.log &"
    openremote --id $controller_id --hive $beehive_url --path $or_base_path --console.threshold.level $log_level &
    echo -n $(get_openremote_current_ver) > $OR_VER_FILE
    cd $saved_pwd
}

prepare_event_processor_config() {
    local email=$1
    local token=$2
    local nimbitsUrl=$3
    mkdir -p $EVENT_PROCESSOR_CONFIG_FILE_DIR
    cat > $EVENT_PROCESSOR_CONFIG_FILE <<EOF
<?xml version="1.0" encoding="UTF-8"?>
<nimbits>
    <email>$email</email>
    <token>$token</token>
    <url>$nimbitsUrl</url>
</nimbits>
EOF

}

prepare_beehive_credentials() {
    local user=$1
    local password=$2
    local beehive_config_files_dir=${3:-$BEEHIVE_CONFIG_FILES_DIR}
    local beehive_config_user_file=${4:-$BEEHIVE_CONFIG_USER_FILE}
    local beehive_config_password_file=${5:-$BEEHIVE_CONFIG_PASSWORD_FILE}
    mkdir -p $beehive_config_files_dir
    
    echo "$user" > $beehive_config_user_file
    echo "$password" > $beehive_config_password_file
    
   cat > $OR_WEBAPPS_SECURITY_USERS <<EOF
<?xml version='1.0' encoding='utf-8'?>
<tomcat-users>
  <role rolename="openremote"/>
  <user username="$user" password="$password" roles="openremote"/>
</tomcat-users>
EOF

}

prepare_configuration() {
    local nimbits_email=${1:-unknown_email}
    local nimbits_token=${2:-unknown_token}
    local nimbits_url=${3:-unknown_url}
    local beehive_user=${4:-unknown_user}
    local beehive_password=${5:-unknown_password}
    
    prepare_event_processor_config $nimbits_email $nimbits_token $nimbits_url
    prepare_beehive_credentials $beehive_user $beehive_password
    mkdir -p $OR_CONFIG_RULES_DIR
}

main() {
    if openremote_is_running; then 
        is_or_running=1
    else
        is_or_running=0
    fi
    or_running_ver=$(get_openremote_running_ver)
    or_current_ver=$(get_openremote_current_ver)
    hms_enabled=$(get_hms_enabled)
    hms_nimbits_email=$(get_hms_nimbits_email)
    hms_nimbits_token=$(get_hms_nimbits_token)
    hms_nimbits_url=$(get_hms_nimbits_url)
    hms_beehive_user=$(get_hms_beehive_user)
    hms_beehive_password=$(get_hms_beehive_password)
    hms_beehive_url=$(get_hms_beehive_url)
    hms_log_level=$(get_hms_log_level)
    hms_controller_id=$(get_hms_controller_id)
#    debug "OR(siege) is running: $is_or_running; Running ver: $or_running_ver; Current ver: $or_current_ver; "\#        "HMS enabled: $hms_enabled; Nimbits email: $hms_nimbits_email; Nimbits token: $hms_nimbits_token; "\
#  "Beehive user: $hms_beehive_user; Beehive password: $hms_beehive_password; Controller id: $hms_controller_id"

    if ! [ "$hms_enabled" = "1" ]; then
        if [ "$is_or_running" = "1" ]; then
            stop_running_openremote
        fi
        return 0
    fi

    # hms_enabled == 1
    if [ "$or_running_ver" = "$or_current_ver" ]; then
        return 0
    fi

    # hms_enabled == 1 and or_running_ver != or_current_ver
    if [ "$is_or_running" = "1" ]; then 
        stop_running_openremote
        sleep 1
    fi
    prepare_configuration $hms_nimbits_email $hms_nimbits_token $hms_nimbits_url $hms_beehive_user $hms_beehive_password
    start_current_openremote $hms_controller_id $hms_beehive_url $hms_log_level
}

case "$1" in
  getcurversion)
	    get_openremote_current_ver
        ;;
  getrunningversion)
	    get_openremote_running_ver
        ;;
  stop)
        hms_enabled=$(get_hms_enabled)
		if [ "$hms_enabled" = "1" ]; then
			if openremote_is_running; then
				stop_running_openremote
				echo "openremote stop has been performed";
			else
                echo "openremote is not running";
			fi
			return 0
		else
           echo "HMS is not enabled in config";
		fi
        ;;
  status)
        if ! [ -e $(readlink $OR_CURRENT_LINK)/$OR_BIN_RELPATH ]; then
		  echo "openremote is not installed";
        elif openremote_is_running; then
		  echo "openremote is running";
		else
		  echo "openremote is not running";
		fi
        ;;
  *)
    main "$@"
esac
return 0

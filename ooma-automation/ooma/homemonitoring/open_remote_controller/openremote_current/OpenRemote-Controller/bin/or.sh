#!/bin/sh
#SIEGEHOME=/ipkg/siege
#export SIEGEHOME

orLaunch="siege"

orDirName="OpenRemote-Controller"
orPath="/ipkg/"

orHiveRoot="http://designer.openremote.com/"
orHiveRemoteCommand="remote/"
orHiveSync="beehive/rest/"
orHiveDeviceDiscovery="dds/rest/"

orControllerID="1"

tomcatLogLevel="INFO"
orStartupLevel="DEBUG"
orConsoleThreshold="DEBUG"

while [ "$1" != "" ]; do
    
        # Use NFS path
    if [ "$1" == "--nfs" ]
    then
        orPath="/"
        shift
        continue
    fi

        # Set hive
    if [ "$1" == "--hive" ]
    then
        orHiveRoot="$2"
        shift
        shift
        continue
    fi

        # Set remote command service subpath
    if [ "$1" == "--remote" ]
    then
        orHiveRemoteCommand="$2"
        shift
        shift
        continue
    fi 

        # Set sync sub path
    if [ "$1" == "--sync" ]
    then
        orHiveSync="$2"
        shift
        shift
        continue
    fi

        # Set device discovery subpath
    if [ "$1" == "--discovery" ]
    then
        orHiveDeviceDiscovery="$2"
        shift
        shift
        continue
    fi 

        # Set controller id
    if [ "$1" == "--id" ]
    then
        orControllerID="$2"
        shift
        shift
        continue
    fi    

        # Set tomcat.server.console.log.level
    if [ "$1" == "--tomcat.log.level" ]
    then
        tomcatLogLevel="$2"
        shift
        shift
        continue
    fi 

        # Set controller id
    if [ "$1" == "--startup.log.level" ]
    then
        orStartupLevel="$2"
        shift
        shift
        continue
    fi 

        # Set openremote.controller.console.threshold
    if [ "$1" == "--console.threshold.level" ]
    then
        orConsoleThreshold="$2"
        shift
        shift
        continue
    fi 
    
        # clear launch flag
    if [ "$1" == "--nolaunch" ]
    then
        orLaunch="echo"
        shift
        continue
    fi 
done

orRoot="${orPath}${orDirName}"

${orLaunch} -Duser.timezone=$TZ \
	-Dceej.net.ssl.enable.tls=1 \
    -Dcatalina.home="${orRoot}/" \
    -Dcatalina.base="${orRoot}" \
    -Djava.io.tmpdir="${orRoot}/temp" \
    -Dtomcat.server.console.log.level=${tomcatLogLevel} \
    -Dopenremote.controller.startup.log.level=${orStartupLevel} \
    -Dopenremote.controller.console.threshold=${orConsoleThreshold} \
    -Djava.library.path=${orRoot}/webapps/controller/WEB-INF/lib/native \
    -Djava.util.logging.config.file=${orRoot}/conf/logging.properties \
    -Djava.util.logging.manager=org.apache.juli.ClassLoaderLogManager \
    -Dopenremote.remote.command.service.uri="${orHiveRoot}${orHiveRemoteCommand}" \
    -Dopenremote.controller.id=${orControllerID} \
    -Dopenremote.device.discovery.service.uri="${orHiveRoot}${orHiveDeviceDiscovery}" \
    -Dopenremote.sync.service.uri="${orHiveRoot}${orHiveSync}" \
    -cp ":${orRoot}/bin/tomcat/bootstrap.jar:${orRoot}/bin/tomcat/tomcat-juli.jar" \
    org.apache.catalina.startup.Bootstrap start

#siege -Duser.timezone=$TZ \
#-Dcatalina.home=/ipkg/OpenRemote-Controller/ \
#-Dcatalina.base=/ipkg/OpenRemote-Controller \
#-Djava.io.tmpdir=/ipkg/OpenRemote-Controller/temp \
#-Dtomcat.server.console.log.level=INFO \
#-Dopenremote.controller.startup.log.level=DEBUG \
#-Dopenremote.controller.console.threshold=DEBUG \
#-Djava.library.path=/ipkg/OpenRemote-Controller/webapps/controller/WEB-INF/lib/native \
#-Djava.util.logging.config.file=/ipkg/OpenRemote-Controller/conf/logging.properties \
#-Djava.util.logging.manager=org.apache.juli.ClassLoaderLogManager \
#-Dopenremote.remote.command.service.uri="https://beehive.openremote.org/remote" \
#-Dopenremote.controller.id="1" \
#-Dopenremote.device.discovery.service.uri="https://beehive.openremote.org/dds/rest/" \
#-Dopenremote.sync.service.uri="https://beehive.openremote.org/3.0/alpha5/rest/" \
#-cp ":/ipkg/OpenRemote-Controller/bin/tomcat/bootstrap.jar:/ipkg/OpenRemote-Controller/bin/tomcat/tomcat-juli.jar" \
#org.apache.catalina.startup.Bootstrap start

# Other debug defines
#-Djava.net.url.debug="all"
#-Dceej.debug
#-Dceej.net.ssl.norootcerts=1
#-Dceej.net.ssl.certfiledir="/ipkg/certs/"
#-Dceej.net.ssl.verbose=1
#-Djava.security.debug="all"
#-Dceej.debug.displayurl=1
#-Djava.net.url.debug=1


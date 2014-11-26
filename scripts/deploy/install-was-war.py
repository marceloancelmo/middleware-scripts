# Script que faz a instalacao e inicializacao de uma aplicacao em um servidor WebSphere, pode ser executado via wsadmin com a seguinte linha de comando
# wsadmin.bat -lang jython -conntype SOAP -host [hostname] -port [soap_port] -user [was_user] -password [was_pwd] -f [path]/install-was-war.py [appname] [appear] [nodeName] [serverName] [contextRoot]
# Os argumentos passados apos o nome do script sao os seguintes:
# 1 - Nome da aplicacao dentro do WebSphere
# 2 - Local onde se encontra o EAR da aplicacao
# 3 - Nome do no onde se encontra o servidor
# 4 - Nome do servidor que ira executar a aplicacao

appexists = AdminApplication.checkIfAppExists(sys.argv[0])

if (appexists == "false"):
	print "Installing the application " + sys.argv[0]
    #TODO: Retrieve cellname and HTTP server name from configuration
    #TODO: move the not changing parameters to another variable
	# Installing application
	AdminApp.install(sys.argv[1], '[ -nopreCompileJSPs -distributeApp -nouseMetaDataFromBinary -nodeployejb -appname sys.argv[0] -createMBeansForResources -noreloadEnabled -nodeployws -validateinstall warn -noprocessEmbeddedConfig -filepermission .*\.dll=755#.*\.so=755#.*\.a=755#.*\.sl=755 -noallowDispatchRemoteInclude -noallowServiceRemoteInclude -asyncRequestDispatchType DISABLED -nouseAutoLink -noenableClientModule -clientMode isolated -novalidateSchema -contextroot /sys.argv[4] -MapModulesToServers [[ bb/com/br/alm sys.argv[1],WEB-INF/web.xml WebSphere:cell=lepz0129Cell01,node=sys.argv[2],server=IHS-8+WebSphere:cell=lepz0129Cell01,node=sys.argv[2],server=sys.argv[3] ]] -MapWebModToVH [[ bb/com/br/alm sys.argv[1],WEB-INF/web.xml default_host ]] -CtxRootForWebMod [[ bb/com/br/alm sys.argv[1],WEB-INF/web.xml /sys.argv[4] ]]]' )
else:
	print "Application " + sys.argv[0] + " already installed, updating to new version"

	# Parando a aplicacao
	AdminApplication.stopApplicationOnSingleServer(sys.argv[0], sys.argv[2], sys.argv[3])
	
	# Executando o update da aplicacao
	AdminApplication.updateApplicationUsingDefaultMerge(sys.argv[0], sys.argv[1])
#endIf

# Salvando a instalacao da aplicacao na configuracao master do WebSphere
AdminUtilities.save()

# Fazendo a sincronizacao do no 
AdminNodeManagement.syncNode(sys.argv[2])

# Iniciando a aplicacao
AdminApplication.startApplicationOnSingleServer(sys.argv[0], sys.argv[2], sys.argv[3])
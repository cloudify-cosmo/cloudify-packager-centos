# flake8: NOQA
########
# Copyright (c) 2014 GigaSpaces Technologies Ltd. All rights reserved
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
#    * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    * See the License for the specific language governing permissions and
#    * limitations under the License.

from user_definitions import *

# TODO: add support for "skip_get" and "skip_pack" flags.
PACKAGES = {
    "cloudify-core": {
        "name": "cloudify-core",
        "version": "3.0.0",
        "depends": [
            'cloudify-components'
        ],
        "package_path": "/cloudify",
        "sources_path": CORE_PACKAGES_PATH,
        "src_package_type": "dir",
        "dst_package_type": "rpm",
        "bootstrap_script_in_pkg": "{0}/cloudify-core-bootstrap.sh".format(SCRIPTS_PATH),
        "bootstrap_template": "cloudify-core-bootstrap.template",
        "bootstrap_log": "/var/log/cloudify-core-bootstrap.log",
        "overwrite_package": False,
        "config_templates": {
            "__params_celery": {
                "init_path": "/etc/init/celeryd-cloudify-management.conf",
                "run_dir": "{0}/celery".format(VIRTUALENVS_PATH),
            },
            "__params_manager": {
                "port": "8100",
            },
            "__params_workflow": {
                "port": "8101",
            },
        }
    },
    "cloudify-components": {
        "name": "cloudify-components",
        "version": "3.0.0",
        "package_path": "/cloudify",
        "sources_path": COMPONENT_PACKAGES_PATH,
        "src_package_type": "dir",
        "dst_package_type": "rpm",
        "bootstrap_script_in_pkg": "{0}/cloudify-components-bootstrap.sh".format(SCRIPTS_PATH),
        "bootstrap_template": "cloudify-components-bootstrap.template",
        "bootstrap_log": "/var/log/cloudify-bootstrap.log",
        "overwrite_package": False,
        "bootstrap_params": {
            "req_free_mem": "10000",
            "req_free_disk": "5",
            "req_cpu_cores": "1",
            "req_arch": "x86_64",
            "req_os": "CentOS release 6.4 (Final)",
        },
        "config_templates": {
            "__template_file_nginx": {
                "template": "{0}/nginx/default.conf.template".format(CONFIGS_PATH),
                "output_file": "default.conf",
                "config_dir": "config/nginx",
                "dst_dir": "/etc/nginx/conf.d",
            },
            "__params_nginx": {
                "kibana_run_dir": "/opt/kibana3",
                "kibana_port": "3000",
                "rest_and_ui_port": "80",
                "file_server_port": "53229",
                "file_server_dir": "{0}/manager/resources".format(VIRTUALENVS_PATH),
            },
            "__params_rabbitmq": {
                "port": "5672"
            },
            "__params_logstash": {
                "port": "9999"
            },
            "__params_elasticsearch": {
                "port": "9200"
            },
            "__template_dir_riemann": {
                "templates": "{0}/riemann/conf".format(CONFIGS_PATH),
                "config_dir": "config/riemann/conf",
                "dst_dir": "/etc/riemann",
            },
            "__params_riemann": {
                "ws_port": "5556",
                "tcp_port": "5555",
            },
            "__template_file_riemann": {
                "template": "{0}/riemann/init/riemann.conf.template".format(CONFIGS_PATH),
                "config_dir": "config/riemann/init",
                "dst_dir": "/etc/init/riemann.conf",
            },
            "__params_ruby": {
                "run_dir": "/opt/ruby",
            },
            "__template_file_rabbitmq": {
                "template": "{0}/rabbitmq/init/rabbitmq-server.conf.template".format(CONFIGS_PATH),
                "config_dir": "config/rabbitmq",
                "dst_dir": "/etc/init/rabbitmq-server.conf",
            },
        }
    },
    "cloudify-ui": {
        "name": "cloudify-ui",
        "version": "1.0.0",
        "source_urls": [
            "http://builds.gsdev.info/cosmo-ui/1.0.0/cosmo-ui-1.0.0-latest.tgz",
        ],
        "depends": [
            'nodejs'
        ],
        "package_path": "/cloudify",
        "sources_path": "{0}/cloudify-ui".format(PACKAGES_PATH),
        "src_package_type": "dir",
        "dst_package_type": "rpm",
        "bootstrap_script": "{0}/cloudify-ui-bootstrap.sh".format(SCRIPTS_PATH),
        "bootstrap_template": "cloudify-ui-bootstrap.template",
        "bootstrap_log": "/var/log/cloudify-bootstrap.log",
        "config_templates": {
            "__template_file_init": {
                "template": "{0}/cloudify-ui/init/cloudify-ui.conf.template".format(CONFIGS_PATH),
                "output_file": "cloudify-ui.conf",
                "config_dir": "config/init",
                "dst_dir": "/etc/init",
            },
            "__params_init": {
                "log_file": "/var/log/cloudify-ui/cosmo-ui.log",
                "user": "root",
                "run_dir": "/opt/cloudify-ui",
            },
            "__params_ui": {
                "port": "9001",
            },
        }
    },
    "centos-agent-archive": {
        "name": "centos-agent",
        "version": "3.0.0",
        "package_path": "/cloudify",
        "sources_path": "{0}/centos-agent".format(AGENT_PACKAGES_PATH),
        "src_package_type": "dir",
        "dst_package_types": ["rpm", "deb"],
        "bootstrap_script": "{0}/agent-centos-bootstrap.sh".format(SCRIPTS_PATH),
        "bootstrap_template": "agent-centos-bootstrap.template",
        "bootstrap_params": {
            "file_server_path": "{0}/manager/resources".format(VIRTUALENVS_PATH),
            "dst_agent_location": "packages/agents",
            "dst_template_location": "packages/templates",
            "dst_script_location": "packages/scripts"
        },
        "bootstrap_log": "/var/log/cloudify3-bootstrap.log",
        # TODO: CREATE INIT AND DEFAULTS FILES FROM TEMPLATES!
        "config_templates": {
            "__config_dir": {
                "files": "{0}/centos-agent".format(CONFIGS_PATH),
                "config_dir": "config",
                "dst_dir": "{0}/manager/resources/packages/agents/templates/".format(VIRTUALENVS_PATH),
            },
        },
    },
    "centos-agent": {
        "name": "centos-agent",
        "version": "3.0.0",
        "source_urls": [
            "https://github.com/cloudify-cosmo/cloudify-manager/archive/{0}.tar.gz".format(MAIN_BRANCH),
        ],
        "package_path": "{0}/centos-agent".format(AGENT_PACKAGES_PATH),
        "sources_path": "/centos-agent/env",
        "modules": ['billiard==2.7.3.28', 'celery==3.0.24', 'bernhard', 'pika',
                    'https://github.com/cloudify-cosmo/cloudify-rest-client/archive/{0}.tar.gz'.format(MAIN_BRANCH),
                    'https://github.com/cloudify-cosmo/cloudify-plugins-common/archive/{0}.tar.gz'.format(MAIN_BRANCH),
                    '/centos-agent/env/cloudify-manager-{0}/plugins/agent-installer/'.format(MAIN_BRANCH),
                    '/centos-agent/env/cloudify-manager-{0}/plugins/plugin-installer/'.format(MAIN_BRANCH),
        ],
        "src_package_type": "dir",
        "dst_package_types": ["tar.gz"],
    },
    "manager": {
        "name": "manager",
        "version": "3.0.0",
        "source_urls": [
            "https://github.com/cloudify-cosmo/cloudify-manager/archive/{0}.tar.gz".format(MAIN_BRANCH),
        ],
        "depends": [
            'ruby2.1'
        ],
        "package_path": "{0}/manager/".format(CORE_PACKAGES_PATH),
        "sources_path": "{0}/manager".format(VIRTUALENVS_PATH),
        "modules": [
            '{0}/manager/cloudify-manager-{1}/rest-service/'.format(VIRTUALENVS_PATH, MAIN_BRANCH),
            '{0}/manager/cloudify-manager-{1}/plugins/agent-installer/'.format(VIRTUALENVS_PATH, MAIN_BRANCH),
            '{0}/manager/cloudify-manager-{1}/plugins/plugin-installer/'.format(VIRTUALENVS_PATH, MAIN_BRANCH),
        ],
        "resources_path": "{0}/manager/cloudify-manager-{1}/resources/rest-service/cloudify/".format(VIRTUALENVS_PATH, MAIN_BRANCH),
        "file_server_dir": "{0}/manager/resources".format(VIRTUALENVS_PATH),
        "src_package_type": "dir",
        "dst_package_type": "rpm",
        "bootstrap_script": "{0}/manager-bootstrap.sh".format(SCRIPTS_PATH),
        "bootstrap_template": "manager-bootstrap.template",
        "bootstrap_params": {
            "resources_dir_src": "cosmo-manager-*/orchestrator/src/main/resources/cloudify/",
            "resources_dir_dst": "filesrv",
            "alias_file_src": "cosmo-manager-*/orchestrator/src/main/resources/org/CloudifySource/cosmo/dsl/alias-mappings.yaml",
            "alias_file_dst": "filesrv/cloudify",
        },
        "config_templates": {
            "#__template_file_init_gunicorn": {
                "template": "{0}/manager/init/manager.conf.template".format(CONFIGS_PATH),
                "output_file": "manager.conf",
                "config_dir": "config/init",
                "dst_dir": "/etc/init",
            },
            "#__template_file_init_workflow": {
                "template": "{0}/manager/init/workflow.conf.template".format(CONFIGS_PATH),
                "output_file": "manager.conf",
                "config_dir": "config/init",
                "dst_dir": "/etc/init",
            },
            "__params_init": {
                "rest_server_path": "{0}/manager/cloudify-manager-{1}/rest-service/manager_rest/".format(VIRTUALENVS_PATH, MAIN_BRANCH),
                "gunicorn_user": "root",
                "gunicorn_conf_path": "{0}/manager/config/conf/guni.conf".format(VIRTUALENVS_PATH),
                "unicorn_user": "root",
                "ruby_path": "{0}/ruby".format(VIRTUALENVS_PATH),
                "workflow_service_path": "{0}/manager/cloudify-manager-{1}/workflow-service/".format(VIRTUALENVS_PATH, MAIN_BRANCH),
                "workflow_service_logs_path": "/var/log/cosmo/blueprints",
                "ruote_storage_dir_path": "/var/ruotefs",
            },
            "__template_file_conf": {
                "template": "{0}/manager/conf/guni.conf.template".format(CONFIGS_PATH),
                "output_file": "guni.conf",
                "config_dir": "config/conf",
                # "dst_dir": "/opt/manager/config/conf",
            },
            "__params_conf": {
                "file_server_dir": "{0}/manager/resources".format(VIRTUALENVS_PATH),
            },
            "__template_dir_init": {
                "templates": "{0}/manager/init".format(CONFIGS_PATH),
                "config_dir": "config/init",
                "dst_dir": "/etc/init",
            },
        }
    },
    "celery": {
        "name": "celery",
        "version": "0.0.1",
        "source_urls": [
            "https://github.com/cloudify-cosmo/cloudify-manager/archive/{0}.tar.gz".format(MAIN_BRANCH),
        ],
        "package_path": "{0}/celery/".format(CORE_PACKAGES_PATH),
        "sources_path": "{0}/celery/cloudify.management__worker/env".format(VIRTUALENVS_PATH),
        "modules": ['billiard==2.7.3.28', 'celery==3.0.24', 'bernhard', 'pika',
                    '{0}/celery/cloudify.management__worker/env/cloudify-manager-{1}/plugins/agent-installer/'.format(VIRTUALENVS_PATH, MAIN_BRANCH),
                    '{0}/celery/cloudify.management__worker/env/cloudify-manager-{1}/plugins/plugin-installer/'.format(VIRTUALENVS_PATH, MAIN_BRANCH),
                    'https://github.com/cloudify-cosmo/cloudify-plugins-common/archive/{0}.tar.gz'.format(MAIN_BRANCH),
        ],
        "src_package_type": "dir",
        "dst_package_type": "rpm",
        "bootstrap_script": "{0}/celery-bootstrap.sh".format(SCRIPTS_PATH),
        "bootstrap_template": "celery-bootstrap.template",
        "config_templates": {
            "__template_file_init": {
                "template": "{0}/celery/init/celeryd-cloudify-management.conf.template".format(CONFIGS_PATH),
                "output_file": "celeryd-cloudify-management.conf",
                "config_dir": "config/init",
                "dst_dir": "/etc/init",
            },
            "__params_init": {
                "work_dir": "{0}/celery/cloudify.management__worker".format(VIRTUALENVS_PATH),
                "base": "/opt/celery",
                "rest_port": "8100",
                "file_server_port": "53229",
            },
        }
    },
    "logstash": {
        "name": "logstash",
        "version": "1.3.2",
        "source_urls": [
            "https://download.elasticsearch.org/logstash/logstash/logstash-1.3.2-flatjar.jar",
        ],
        "depends": [
            'java-1.7.0-openjdk'
        ],
        "package_path": "{0}/logstash/".format(COMPONENT_PACKAGES_PATH),
        "sources_path": "{0}/logstash".format(PACKAGES_PATH),
        "src_package_type": "dir",
        "dst_package_type": "rpm",
        "bootstrap_script": "{0}/logstash-bootstrap.sh".format(SCRIPTS_PATH),
        "bootstrap_template": "logstash-bootstrap.template",
        "config_templates": {
            "__template_file_init": {
                "template": "{0}/logstash/init/logstash.conf.template".format(CONFIGS_PATH),
                "output_file": "logstash.conf",
                "config_dir": "config/init",
                "dst_dir": "/etc/init",
            },
            "__params_init": {
                "jar": "logstash.jar",
                "log_file": "/var/log/logstash.out",
                "conf_path": "/etc/logstash.conf",
                "run_dir": "/opt/logstash",
                "user": "root",
            },
            "__template_file_conf": {
                "template": "{0}/logstash/conf/logstash.conf.template".format(CONFIGS_PATH),
                "output_file": "logstash.conf",
                "config_dir": "config/conf",
                "dst_dir": "/etc",
            },
            "__params_conf": {
                "events_queue": "cloudify-events",
                "logs_queue": "cloudify-logs",
                "test_tcp_port": "9999",
                "events_index": "cloudify_events",
            }
        }
    },
    "elasticsearch": {
        "name": "elasticsearch",
        "version": "1.0.1",
        "source_urls": [
            "https://download.elasticsearch.org/elasticsearch/elasticsearch/elasticsearch-1.0.1.tar.gz",
        ],
        "depends": [
            'java-1.7.0-openjdk'
        ],
        "package_path": "{0}/elasticsearch/".format(COMPONENT_PACKAGES_PATH),
        "sources_path": "{0}/elasticsearch".format(PACKAGES_PATH),
        "src_package_type": "dir",
        "dst_package_type": "rpm",
        "bootstrap_script": "{0}/elasticsearch-bootstrap.sh".format(SCRIPTS_PATH),
        "bootstrap_template": "elasticsearch-bootstrap.template",
        "config_templates": {
            "__template_file_init": {
                "template": "{0}/elasticsearch/init/elasticsearch.conf.template".format(CONFIGS_PATH),
                "output_file": "elasticsearch.conf",
                "config_dir": "config/init",
                "dst_dir": "/etc/init",
            },
            "__params_init": {
                "run_dir": "/opt/elasticsearch",
                "user": "root",
            },
            "__template_file_conf": {
                "template": "{0}/elasticsearch/init/elasticsearch.conf.template".format(CONFIGS_PATH),
                "output_file": "elasticsearch.conf",
                "config_dir": "config/conf",
                "dst_dir": "/etc/init",
            },
            "__params_conf": {
            }
        }
    },
    "kibana3": {
        "name": "kibana3",
        "version": "3.0.0milestone4",
        "source_urls": [
            "https://download.elasticsearch.org/kibana/kibana/kibana-3.0.0milestone4.tar.gz",
        ],
        "depends": [
            'java-1.7.0-openjdk',
            'logstash',
            'elasticsearch'
        ],
        "package_path": "{0}/kibana3/".format(COMPONENT_PACKAGES_PATH),
        "sources_path": "{0}/kibana3".format(PACKAGES_PATH),
        "src_package_type": "dir",
        "dst_package_type": "rpm",
        "bootstrap_script": "{0}/kibana-bootstrap.sh".format(SCRIPTS_PATH),
        "bootstrap_template": "kibana-bootstrap.template",
    },
    "nginx": {
        "name": "nginx",
        "version": "1.5.8",
        "reqs": [
            "nginx",
            # "libcrypto.so.10",
            # "libssl.so.10",
            # "openssl",
        ],
        "source_repos": ["http://nginx.org/packages/centos/6/noarch/RPMS/nginx-release-centos-6-0.el6.ngx.noarch.rpm"],
        "package_path": "{0}/nginx/".format(COMPONENT_PACKAGES_PATH),
        "sources_path": "{0}/nginx".format(PACKAGES_PATH),
        "dst_package_type": "rpm",
    },
    "rabbitmq-server": {
        "name": "rabbitmq-server",
        "version": "0.0.1",
        "source_urls": ["https://www.rabbitmq.com/releases/rabbitmq-server/v3.2.4/rabbitmq-server-3.2.4-1.noarch.rpm"],
        "source_repos": ["http://repos.fedorapeople.org/repos/peter/erlang/epel-erlang.repo"],
        "reqs": [
            "erlang"
        ],
        "package_path": "{0}/rabbitmq-server/".format(COMPONENT_PACKAGES_PATH),
        "sources_path": "{0}/rabbitmq-server".format(PACKAGES_PATH),
        "dst_package_type": "rpm"
    },
    "riemann": {
        "name": "riemann",
        "version": "0.2.2",
        "reqs": [
            "daemonize",
        ],
        "source_urls": [
            "http://aphyr.com/riemann/riemann-0.2.2-1.noarch.rpm",
        ],
        "depends": [
            'java-1.7.0-openjdk'
        ],
        "package_path": "{0}/riemann/".format(COMPONENT_PACKAGES_PATH),
        "sources_path": "{0}/riemann".format(PACKAGES_PATH),
        "dst_package_type": "rpm"
    },
    "nodejs": {
        "name": "nodejs",
        "version": "0.0.1",
        "reqs": [
            "openssl-devel",
            # "zlib-devel",
            "libcrypto.so.10",
            # "libssl.so.10",
            # "krb5-devel",
            # "openssl",
        ],
        "source_keys": ["https://fedoraproject.org/static/0608B895.txt"],
        "source_repos": ["http://download-i2.fedoraproject.org/pub/epel/6/i386/epel-release-6-8.noarch.rpm"],
        "package_path": "{0}/nodejs/".format(COMPONENT_PACKAGES_PATH),
        "sources_path": "{0}/nodejs".format(PACKAGES_PATH),
        "dst_package_type": "rpm",
        # "prereqs": ['python-software-properties', 'g++', 'make']
    },
    "java-1.7.0-openjdk": {
        "name": "java-1.7.0-openjdk",
        "version": "0.0.1",
        "reqs": [
            "java-1.7.0-openjdk"
        ],
        "package_path": "{0}/java-1.7.0-openjdk/".format(COMPONENT_PACKAGES_PATH),
        "sources_path": "{0}/java-1.7.0-openjdk".format(PACKAGES_PATH),
        "dst_package_type": "rpm",
    },
    "virtualenv": {
        "name": "virtualenv",
        "version": "1.11.4",
        "package_path": "{0}/virtualenv/".format(COMPONENT_PACKAGES_PATH),
        "sources_path": "{0}/virtualenv".format(PACKAGES_PATH),
        "modules": [
            'virtualenv==1.11.4'
        ],
        "src_package_type": "dir",
        "dst_package_type": "rpm",
        "bootstrap_script": "{0}/virtualenv-bootstrap.sh".format(SCRIPTS_PATH),
        "bootstrap_template": "virtualenv-bootstrap.template"
    },
    # "graphite": {
    #     "name": "graphite",
    #     "version": "0.9.12",
    #     "package_path": "{0}/graphite/".format(COMPONENT_PACKAGES_PATH),
    #     "sources_path": "{0}/graphite".format(VIRTUALENVS_PATH),
    #     "modules": [
    #         'carbon==0.9.10',
    #         'whisper==0.9.12',
    #         'graphite-web==0.9.12'
    #     ],
    #     "src_package_type": "dir",
    #     "dst_package_type": "rpm",
    #     "bootstrap_script": "{0}/graphite-bootstrap.sh".format(SCRIPTS_PATH),
    #     "bootstrap_template": "graphite-bootstrap.template"
    # },
    "curl": {
        "name": "curl",
        "version": "0.0.1",
        "reqs": [
            "curl",
            "libcurl",
        ],
        "package_path": "{0}/curl/".format(COMPONENT_PACKAGES_PATH),
        "sources_path": "{0}/curl".format(PACKAGES_PATH),
        "dst_package_type": "rpm",
    },
    "make": {
        "name": "make",
        "version": "0.0.1",
        "reqs": [
            "make"
        ],
        "package_path": "{0}/make/".format(COMPONENT_PACKAGES_PATH),
        "sources_path": "{0}/make".format(PACKAGES_PATH),
        "dst_package_type": "rpm",
    },
    "ruby": {
        "name": "ruby2.1",
        "version": "2.1.0",
        "package_path": "{0}/ruby/".format(COMPONENT_PACKAGES_PATH),
        "sources_path": "{0}/ruby".format(VIRTUALENVS_PATH),
        "src_package_type": "dir",
        "dst_package_type": "rpm",
        "prereqs": [
            'make',
            'git',
        ],
        "ruby_build_dir": "/opt/ruby-build"
    },
    "workflow-gems": {
        "name": "workflow-gems",
        "version": "0.0.1",
        "source_urls": [
            "https://github.com/cloudify-cosmo/cloudify-manager/archive/{0}.tar.gz".format(MAIN_BRANCH),
        ],
        "depends": [
            'ruby2.1'
        ],
        "gemfile_location": "{0}/workflow-gems/cloudify-manager-{1}/workflow-service/Gemfile".format(PACKAGES_PATH, MAIN_BRANCH),
        "gemfile_base_dir": "{0}/workflow-gems/cloudify-manager-{1}".format(PACKAGES_PATH, MAIN_BRANCH),
        "package_path": "{0}/workflow-gems/".format(COMPONENT_PACKAGES_PATH),
        "sources_path": "{0}/workflow-gems".format(PACKAGES_PATH),
        "src_package_type": "dir",
        "dst_package_type": "rpm",
        "prereqs": [
            'make'
        ],
        "bootstrap_script": "{0}/workflow-gems-bootstrap.sh".format(SCRIPTS_PATH),
        "bootstrap_template": "workflow-gems-bootstrap.template"
    },
}

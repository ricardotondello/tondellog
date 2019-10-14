import gitlab
from datetime import date

class ChangeLogGenerator(object):
    MAIN_TEMPLATE='''# {project} - {group}

## [{release_name}] - {date_today}

### Major
* Breaking Changes

    {breaking_changes}

* Big Features
    
    {big_features}

### Features

{features}
### Bug Fixes

{bug_fixes}
---

### CI/CD

{ci_cds}
### Tests

{tests}
---

### Undefined

{undefined}
'''

    CHANGE_ITEM_TEMPLATE='''    * [{salt_id}] - {title} ({author}) 
{message}'''

    def __init__(self, host, group, project, user=None, password=None, private_token=None, output='CHANGELOG.md'):
        self.host = host
        self.user = user
        self.password = password
        self.private_token = private_token
        self.group = group
        self.project = project
        self.output = output

    @classmethod
    def from_config(cls, config, output='CHANGELOG.md'):
        return ChangeLogGenerator(
            host = config.host,
            private_token = config.private_token,
            group = config.group,
            project = config.project,
            output = output,
        )

    def generate(self):
        c = gitlab.Gitlab(self.host, email=self.user, password=self.password, private_token=self.private_token)
        pl = c.projects.list(search=self.project)
        if not pl:
            print("Project %s not found" % self.project)
            return
        p = None

        for pp in pl:
            if pp.namespace['name'] == self.group:
                p = pp
                break
        if not p:
            print("Project in group %s not found" % self.group)
            return

        result = p.repository_compare('master', 'develop')

        breaking_changes = []
        big_features = []
        features = []
        bug_fixes = []
        ci_cds = []
        tests = []
        undefined = []
        
        for commit in result['commits']:
            commit_message = commit["message"].lower()

            if commit_message[0:12] == "merge branch":
                continue
            idx = commit_message.find(":")
            
            if idx > 0:
                prefixo = commit_message[0: idx]
        
            mensagem_formatada = self.gen_change_item(commit) 
            if prefixo == "break:":
                breaking_changes.append(mensagem_formatada)
            elif prefixo == "big:":
                big_features.append(mensagem_formatada)
            elif prefixo == "feat:":
                features.append(mensagem_formatada)
            elif prefixo == "fix:":
                bug_fixes.append(mensagem_formatada)
            elif prefixo == "ci:":
                ci_cds.append(mensagem_formatada)
            elif prefixo == "test:":
                tests.append(mensagem_formatada)
            else:
                undefined.append(mensagem_formatada)

        #write changelog
        changelog = self.MAIN_TEMPLATE.format(
            project=self.project.upper(),
            group=self.group.upper(),
            release_name="Undefined",
            date_today=date.today().strftime("%d/%m/%Y"),
            breaking_changes='\n'.join(breaking_changes),
            big_features='\n'.join(big_features),
            features='\n'.join(features),
            bug_fixes='\n'.join(bug_fixes),
            ci_cds='\n'.join(ci_cds),
            tests='\n'.join(tests),
            undefined='\n'.join(undefined))

        with open(self.output, 'w+') as out:
            out.write(changelog)
            print(f"Changelog is generated to '{self.output}' success.")

    def gen_change_item(self, commit):
        salt_id_start = "id: #"
        salt_id = "299206-1"
        commit_message = commit["message"]
        if commit_message.find(salt_id_start) > 0:
            salt_id = commit_message[commit_message.find(salt_id_start) + len(salt_id_start): commit_message.rfind("\n") ]
        
        title=commit["title"]
        commit_message = commit_message.replace(title + '\n\n', '').replace('\n', ' ').replace(f"{salt_id_start}{salt_id}", '').strip()
        if commit_message:
            commit_message = "      * " + commit_message + '\n'

        return self.CHANGE_ITEM_TEMPLATE.format(
                    salt_id = salt_id,
                    title=title,
                    author=commit["author_name"],
                    message=commit_message)

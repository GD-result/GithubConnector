'''
Created on 29.03.2012

@author: Rezvan aka DreamBit aka John_Pa9JIbHuK

@organization: GridDynamics
'''

STYLE = {'admin': 'font-weight: bold; Color: #D53E07;',
         'push': 'font-weight: bold; Color: #006000;',
         'pull': 'font-weight: normal;'}

def repositoryDesigner(content):
    designContent = '''
                *Repository* - private repository
                Repository - public repository 
                {color:#D53E07}*Team*{color} - team with pull, push & administrative access
                {color:#006000}*Team*{color} - team with push & pull access
                Team - team with pull only access
                h1. Github repositories
                {html}
                <div class='table-wrap'>
                <table width=50% class='confluenceTable'>
                    <tr>
                        <th class='confluenceTh'>Repository</th>
                        <th class='confluenceTh'>Teams</th>
                        <th class='confluenceTh'>Users</th>
                    </tr>
                    '''
    rowColor = "#FBFFE8"
    for repos in content.keys():
        font = "bold" if repos[1] else "normal"
        designContent += "<tr> <td rowspan='%d' style='font-weight: %s; background-color: %s' class='confluenceTd'>%s</td>" % (len(content[repos]), font, rowColor, repos[0])
        if len(content[repos]) == 0:
            designContent += "<td class='confluenceTd' style='background-color: %s'> </td>" % rowColor
            designContent += "<td class='confluenceTd' style='background-color: %s'> </td>" % rowColor
        for team in content[repos]:
            designContent += "<td class='confluenceTd' style='%s background-color: %s'>%s</td>" % (STYLE[team['permission']], rowColor, team['name'])
            designContent += "<td class='confluenceTd' style='background-color: %s'>%s</td>" % (rowColor, ", ".join(team['users']))
            designContent += "</tr>"
        rowColor = 'white' if rowColor == '#FBFFE8' else '#FBFFE8'
    designContent += "</table></div>{html}"   
    return designContent

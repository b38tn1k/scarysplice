# Scary Splice

For Royal Chant. Because splice can't handle 22 drum tracks.

## Automator Quick Actions

Consists of three automator quick actions:

- make new git project
- pack for git
- unpack for git

You need to add them to Apple Automator yourself. They are not signed, very basic and have no error checking. be careful!

## New Project Setup
After saving a new Ableton session, right click on the Ableton Project Folder. Select the quick action 'make new git project'.

Select the .als file you wish to track, right click and 'pack for git'. You should see a .xml file appear.

In Github Desktop, select 'Add' and 'Add Existing Repository'. Navigate to the Ableton Project Folder, Open and then hit 'Add Repository'. If Github Desktop asks you you would like to create a repository here instead, something is wrong.

Type something in the 'Summary' fiueld in Github Desktop, then click 'Commit to master'. Click 'Publish Repository'.

You can add collaborators on the Github website in the repository settings.

## Sharing Updated Project

When you have finished a project session, collect all and save and close Live. Navigate to the project directory and delete any existing .xmls, right click the .als file. Select the quick action 'pack for git'.

In Github Desktop, make sure all the required files are added, type in a summary and hit 'commit to master'. Then hit Push origin to upload the changes.

## Getting Updated Project

In Github Desktop, select the repository you wish to work on. Click 'Fetch origin'. If anything has changed, you can then click 'Pull origin' to download the updated project.

In Finder, navigate to the project directory, delete the exisiting .als, right click the .xml file and choose the Quick Action 'unpack from git'. This will overwrite the .als file that exists with the up to date project file. Open that .als and make some beautiful music!

# Router Implementation

The script.py file runs one CLI instance of a router.
The expected input is 'python script.py PORT LABEL' where LABEL is the label coresponding to the router in the .config file.
  Run the script in six different CLI instances. It is done this way so the output is organized and not dumped into one CLI.

Because UDP messages are not gaurenteed, the updates from other router might not arive and cause the system to never reach convergence.
Hardcoding a fixed number n as the number of updates would make running the environment a timing challenge for the grader and bad practice
Additionally because it is impossible to prove the lack of an update, the script runs until ^C is pressed.
After ^C is pressed the expected output is displayed.

To reduce on clutter for each of the CLI instances, each instance displays their own view of the config file. If you want to display
it, there is a commented line in the main function






This was developed on VSCode
Made by Landon and Blaine
1001906270 1001629719

explaination of test case 2:
The config file would be inputted with the changed values and the connection between B/D would not be present. This would result in the
distances that previously used that link to have a longer path to other nodes than before.
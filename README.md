## Click Scheduler
A way to set up and loop clicking around on a screen, born out of the frustration of working with obtuse, older software.

### 📖 Contents
+ [About](#about)
+ [Features](#features)
+ [Requirements](#requirements)
+ [Using this circus show](#usage)
+ [Why would you make this](#motivation)

### ❓ About <a name = "about"></a>
Click Scheduler is a graphical interface to create, save and load sequences of precise mouse clicks which can then be looped and executed a set amount of times.

### 🛠️ Features <a name = "features"></a>
- **Moves your mouse to a specific set of on-screen coordinates**
- **It clicks**
- **I mean, what else is there to say? It is called *Click Scheduler*, after all**

### ✅ Prerequisites <a name = "requirements"></a>
+ Python 3.7 or greater
+ Whatever's listed under the [requirements.txt](./requirements.txt)

### ⌨️ Usage <a name = "usage"></a>
Grab the latest release or compile it yourself using any process of your choice if you're fancy like that.  
If you despise compiled binaries and want the true python experience instead, the following should do the trick.
```sh
git clone https://github.com/Randoodl/Click_Scheduler
cd Click_Scheduler
python ./src/main.py
```

If this is your first time running Click Scheduler, it is as simple as figuring out where exactly your pointer needs to be using the `Show Mouse Location` overlay and relaying that information to the Sequence Table. Specify whether to execute a left click or right click and for how long the program should wait after executing said action.  
An example sequence looks a little something like this:  

|Action       |MouseX|MouseY|Delay (ms)|
|:------------|:-----|:-----|:---------|
|Right Click  |10    |10    |500       |
|Left Click   |800   |800   |0         |

Which essentially just right clicks in the top-left corner of the screen, waits half a second, moves down towards the bottom-right, left clicks and finally finishes.
Once set up, indicate how often the sequence should be repeated using the `Max Iterations` field.

> [!TIP]  
> Give the sequence a dry run by setting the `Action` to `Idle` before you start messing with clicks all over the place.

At this point you can optionally save the sequence as a simple .txt file, should you want to load it up again at a later stage.  
After hitting `Start` the sequence will kick off, following a little delay.  
Holding down the `Esc` key will interrupt the sequence.

> [!NOTE]  
> Depending on whatever app you wish to interact with, you might need to run Click Scheduler as root/Administrator

### 🔍 Motivation <a name = "motivation"></a>
Sometimes life hands you a neat, elegant and well-documented program. And sometimes it hands you an API that is so goddamn esoteric it literally makes more sense to just click through endless submenus for hours on end. Click Scheduler arose as a result of the latter.  
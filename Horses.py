# Version 0.12
#
# Written for Python 3

from tkinter import *
from time import time
import sqlite3
from random import randint

class Horses:

    def __init__(self, master):



        # Create database and connect to it
        self.db_connection = sqlite3.connect("Game_Stats.db")
        self.db_cursor = self.db_connection.cursor()

        # Create Stats table if it doesn't exist
        self.db_cursor.execute("""CREATE TABLE IF NOT EXISTS Stats (Timestamp REAL, Win INT, Races INT)""")
        self.db_connection.commit()



        # Rename main window and make it unable to be resized
        master.title("The Racetrack")
        master.resizable(False, False)

        # Create main frame which uses a border to keep sides clear of edges of the main window
        self.mainframe = Frame(master, bd = 10)
        self.mainframe.pack()



        # Set widths to work ----- Does this work?
        self.Right_Width = 230



        # (row,col) = (0,0) of self.mainframe
        # Create introductory text and grid it into self.mainframe
        self.Header_Text = Text(self.mainframe, height = 9, width = 100, wrap = WORD, cursor = "arrow")
        self.Header_Text.insert(END,
                                "Welcome to the racetrack! Your employer has purchased 25 horses, "
                                + "and your job is to determine which ones of the lot are the fastest. "
                                + "You will do this by having the horses race each other on the racetrack. But wait! "
                                + "You forgot your watch at home, and the racetrack's clock is broken, "
                                + "and your cellphone just died, and there's nobody else around, and...\n\n"
                                + "Needless to say, you have your work cut out for you. The track only has "
                                + "five lanes and each lane can only have one horse in it at a time. "
                                + "Use your wits and determine which are the three fastest horses so that "
                                + "the rest can be sent to the glue factory. Good luck!"
                                )
        self.Header_Text.config(state=DISABLED)
        self.Header_Text.grid(row = 0, column = 0, pady = (0,10), sticky = "NW")



        # (row,col) = (0,1) of self.mainframe
        # Create self.frame_Stats and grid it into self.mainframe
        self.frame_Stats = Frame(self.mainframe)
        self.frame_Stats.grid(row = 0, column = 1, pady = (0,10), sticky = "NW")

        # Create and grid "Game Stats" label
        Label(self.frame_Stats, text = "Game Stats").grid(row = 0, column = 0)

        # Create self.frame_Stats_Table and grid it into self.frame_Stats
        self.frame_Stats_Table = Frame(self.frame_Stats)
        self.frame_Stats_Table.grid(row = 1, column = 0)
        
        # Create text for each tracked stat
        self.Game_Stats_Text = (
            "Total number of games:",
            "Total number of wins:",
            "Current winning streak:",
            "Fewest races needed to win:"
            )

        # Make the game stats variables and grid both text and variables into self.frame_Stats_Table
        self.Game_Stats = []
        for rowplace in range(0,4):
            self.Game_Stats.append(StringVar())
            Label(self.frame_Stats_Table, text = self.Game_Stats_Text[rowplace]).grid(row = rowplace, column = 0, sticky = "W")
            Label(self.frame_Stats_Table, textvariable = self.Game_Stats[rowplace]).grid(row = rowplace, column = 1, sticky = "E")

        # Create frame for packing "New Game" and "Reset Stats" buttons into, then grid it into self.frame_Stats
        self.frame_Stats_Buttons = Frame(self.frame_Stats)
        self.frame_Stats_Buttons.grid(row = 2, column = 0, pady = (5,0))

        # Create buttons and pack them into self.frame_Stats_Buttons
        Button(self.frame_Stats_Buttons, text = "New Game", command = self.new_Game).grid(row = 0, column = 0, padx = (0,5))
        Button(self.frame_Stats_Buttons, text = "Reset Stats", command = self.reset_Stats).grid(row = 0, column = 1)



        # (row,col) = (1,0) of self.mainframe
        # Create self.frame_Horses and grid it into self.mainframe
        self.frame_Horses = Frame(self.mainframe)
        self.frame_Horses.grid(row = 1, column = 0, pady = (0,10), sticky = "N")

        # Create and grid "Today's Horses" label
        Label(self.frame_Horses, text = "Today's Horses").grid(row = 0, column = 0)

        # Create self.frame_Horses_Table and grid it into self.frame_Horses
        self.frame_Horses_Table = Frame(self.frame_Horses)
        self.frame_Horses_Table.grid(row = 1, column = 0)
        
        # Create the tuple of horse names
        self.Horse_Names = (
            "Alpha",
            "Brigadier",
            "Chutzpah",
            "Dragonfly",
            "Excalibur",
            "Fame",
            "Ghanima",
            "Hockeye Hickory",
            "Incredibly Idle",
            "Jumping Jack",
            "Kendrasaurus",
            "Lucky",
            "Monty",
            "Nano",
            "Ouroboros",
            "Peanut",
            "Quasar",
            "Rhastamon",
            "Sticky Widget",
            "Terwilliger Tango",
            "Underdog",
            "Vegeta",
            "Why?",
            "Xavier Omar",
            "Yoshi"
            )

        # Create and grid the labels for each horse in self.Horse_Names into self.frame_Horses_Table
        for colplace in range(0,5):
            for rowplace in range(0,5):
                Label(self.frame_Horses_Table, text = "{}.".format(5*colplace+rowplace+1)).grid(row = rowplace, column = 2*colplace, sticky = "E")
                Label(self.frame_Horses_Table, anchor = "w", width = 12, text = self.Horse_Names[5*colplace+rowplace]).grid(row = rowplace, column = 2*colplace+1, padx = (0,10), sticky = "W")



        # (row,col) = (1,1) of self.mainframe
        # Create self.frame_Guesses and grid it into self.mainframe
        self.frame_Guesses = Frame(self.mainframe)
        self.frame_Guesses.grid(row = 1, column = 1, pady = (0,10), sticky = "NW")

        # Create and grid "Which horses are the fastest?" label
        Label(self.frame_Guesses, text = "Which horses are the fastest?").grid(row = 0, column = 0)
        
        # Create self.frame_Guesses_Table and grid it into self.frame_Guesses
        self.frame_Guesses_Table = Frame(self.frame_Guesses)
        self.frame_Guesses_Table.grid(row = 1, column = 0)

        # Create the text for each guess
        self.Guess_Labels = (
            "Fastest:",
            "2nd fastest:",
            "3rd fastest:",
            )

        # Create and grid the labels for each label in self.Guess_Labels into self.frame_Guesses_Table
        # Create self.Guesses and self.Guess_Entries for storing player guesses
        # Grid the entry boxes in self.Guess_Entries into self.frame_Guesses_Table
        self.Guesses = []
        self.Guess_Entries = []
        for rowplace in range(0,3):
            Label(self.frame_Guesses_Table, text = self.Guess_Labels[rowplace]).grid(row = rowplace, column = 0, sticky = "W")
            self.Guesses.append(StringVar())

        # Create self.Guess_Button
        self.Guess_Button = Button(self.frame_Guesses, text = "Report to Employer")


        # (row,col) = (2,0) of self.mainframe
        # Create self.frame_Results and grid it into self.mainframe
        self.frame_Results = Frame(self.mainframe)
        self.frame_Results.grid(row = 2, column = 0, sticky = "NW")

        # Create self.frame_Results_Scrollbox (as a Canvas object) and pack it into self.Results
        self.frame_Results_Scrollbox = Canvas(self.frame_Results, width = 710, highlightcolor = "white")
        self.frame_Results_Scrollbox.pack(fill = X, expand = True)
        
        # Create self.Results_Scrollbar, pack it into self.Results, and tie it to self.frame_Results_Scrollbox
        self.Results_Scrollbar = Scrollbar(self.frame_Results, orient = HORIZONTAL, command = self.frame_Results_Scrollbox.xview)
        self.Results_Scrollbar.pack(fill = X, expand = True)
        self.frame_Results_Scrollbox.config(xscrollcommand = self.Results_Scrollbar.set)

        # Create self.frame_Results_Scrollbox_Display
        self.frame_Results_Scrollbox_Display = Frame(self.frame_Results_Scrollbox)

        # Create a window in self.frame_Results_Scrollbox and display self.frame_Results_Scrollbox_Display in it
        self.frame_Results_Scrollbox.create_window((0,0), window = self.frame_Results_Scrollbox_Display, anchor = "nw")
        self.frame_Results_Scrollbox_Display.bind("<Configure>", self.resize_frame_Results_Scrollbox)
        
        # Create variable to store width of self.frame_Results_Scrollbox_Display to detect when it changes width
        # Used in self.resize_frame_Results_Scrollbox method to determine whether a race has been run or not
        self.Results_Scrollbox_Display_Invoke_Scroll = self.frame_Results_Scrollbox_Display.winfo_width()
        
        # Create lists to store:
        # StringVars for results
        # Buttons for results
        # Entries for results
        self.Results = []
        self.Results_Buttons = []
        self.Results_Entries = []



        # (row,col) = (2,1) of self.mainframe
        # Create self.frame_Messages and grid it into self.mainframe
        self.frame_Messages = Frame(self.mainframe)
        self.frame_Messages.grid(row = 2, column = 1, sticky = "NW")

        # Create "Messages:" label and grid it into self.frame_Messages
        Label(self.frame_Messages, text = "Messages:").grid(row = 0, column = 0, sticky = "W")
        
        # Create self.frame_Messages_Text and grid it into self.frame_Messages
        self.frame_Messages_Text = Frame(self.frame_Messages)
        self.frame_Messages_Text.grid(row = 1, column = 0, sticky = "W")

        # Create self.Messages_Text and pack it into self.frame_Messages_Text on the left
        self.Messages_Text = Text(self.frame_Messages_Text, height = 10, width = 25, wrap = WORD, cursor = "arrow", highlightcolor = "white", state = DISABLED)
        self.Messages_Text.pack(side = LEFT, fill = BOTH, expand = True)

        # Create self.Messages_Scrollbar, pack it into self.frame_Messages_Text on the right, and tie it to self.Messages_Text
        self.Messages_Scrollbar = Scrollbar(self.frame_Messages_Text, orient = VERTICAL, command = self.Messages_Text.yview)
        self.Messages_Scrollbar.pack(side = RIGHT, fill = Y, expand = True)
        self.Messages_Text.config(yscrollcommand = self.Messages_Scrollbar.set)



        # Initialize first game on starting program
        self.print_Message(
            "To play:\n\n"
            + "Type the names of horses you want to race in the boxes on the left, "
            + "then click the button above them. The horses will then be arranged from "
            + "fastest to slowest. When you're ready, type the names of the three fastest "
            + 'horses in the boxes above and click the "Report to Employer" button. '
            + "The game will end and you will find out if you won or lost. "
            + "Try to win while making as few races as possible!\n\n"
            + "(There are also several references in the horse names to Monty Python or its creators' other works. "
            + "Some are obvious, but one is intended to be quite tricky to spot. Can you find them all?)"
            )
        self.new_Game()
        self.Messages_Text.yview_moveto(0)


    
    #
    # Begin methods
    #



    # Method to resize self.frame_Results_Scrollbox, resize its scrollregion,
    # and auto-scroll self.Results_Scrollbar when new results are generated
    # DO NOT MODIFY!
    def resize_frame_Results_Scrollbox(self, event):
        self.frame_Results_Scrollbox.config(height = self.frame_Results_Scrollbox_Display.winfo_height())
        self.frame_Results_Scrollbox.config(scrollregion = self.frame_Results_Scrollbox.bbox("all"))
        if self.Results_Scrollbox_Display_Invoke_Scroll != self.frame_Results_Scrollbox_Display.winfo_width():
            self.Results_Scrollbox_Display_Invoke_Scroll = self.frame_Results_Scrollbox_Display.winfo_width()
            self.frame_Results_Scrollbox.xview_moveto(1)



    # Method to enable self.Guess_Entries boxes
    # DO NOT MODIFY!
    def enable_Guess_Entries(self):
        [guess.set("") for guess in self.Guesses]
        [entry.config(state = NORMAL) for entry in self.Guess_Entries]
        self.Guess_Button.config(state = NORMAL)



    # Method to create new diabled self.Guess_Entries boxes
    # This method will destroy existing boxes and recreate them without clearing their contents
    # DO NOT MODIFY!
    def create_disabled_Guess_Entries(self):
        self.Guess_Button.destroy()
        self.Guess_Button = Button(self.frame_Guesses, text = "Report to Employer", command = self.make_Guess, state = DISABLED)
        self.Guess_Button.grid(row = 2, column = 0, pady = (5,0))
        [entry.destroy() for entry in self.Guess_Entries]
        self.Guess_Entries.clear()
        for rowplace in range(0,3):
            self.Guess_Entries.append(Entry(self.frame_Guesses_Table, textvariable = self.Guesses[rowplace], width = 12, state = DISABLED, cursor = "arrow"))
            self.Guess_Entries[rowplace].grid(row = rowplace, column = 1)
        


    # Actions to take when self.Guess_Button is pressed
    # DO NOT MODIFY!
    def make_Guess(self):
        Guess_List = [entry.get().lower() for entry in self.Guesses]
        if (3 > len(self.remove_Blanks(Guess_List))):
            self.print_Message("You must type a horse's name in each box.")
        elif not (self.check_Valid_Horses(Guess_List)):
            self.print_Message("At least one of these is not a horse. Check spelling, extra spaces, etc.")
        elif (1 < self.check_Duplicate_Horses(Guess_List)):
            self.print_Message("A horse cannot be faster than itself.")
        else:
            self.Game_Over = True
            self.create_disabled_Guess_Entries()
            self.disable_Results_Entries()
            for i in range(0,3):
                Guess_List[i] = self.Horse_Dictionary[Guess_List[i]]
            if Guess_List == [0,1,2]:
                self.print_Message(
                    "\nThe Don is pleased and has promised you some of the profits from the sale of the glue.\n"
                    +"(You did realize that you were working for the mob, right?)\n\n\n"
                    )
                timestamp = self.db_cursor.execute("""SELECT Timestamp FROM Stats ORDER BY Timestamp DESC""").fetchone()[0]
                self.db_cursor.executemany("""UPDATE Stats SET Win = 1, Races = ? WHERE Timestamp = ?""",[(self.Race_Count,timestamp,)])
                self.db_connection.commit()
                self.run_Game_Stats()
            else:
                Top_Horses = [self.Horse_Dictionary[str(i)] for i in range(0,3)]
                self.print_Message(
                    "\nYOU have been sent to the glue factory! "
                    +"(What did you expect would happen when you work for the mob? "
                    +"Who else would invest in racehorses?)\n"
                    +"The winning horses:"
                    )
                [self.print_Message("- "+name) for name in Top_Horses]



    # Method to create new self.Results_Entries boxes
    # DO NOT MODIFY!
    def create_Results_Entries(self):
        self.Race_Count = len(self.Results)
        self.Results.append([StringVar() for i in range(0,5)])
        self.Results_Entries.append([Entry(self.frame_Results_Scrollbox_Display, textvariable = self.Results[self.Race_Count][i], width = 12, cursor = "arrow") for i in range(0,5)])
        self.Results_Buttons.append(Button(self.frame_Results_Scrollbox_Display, text = "Race {}".format(self.Race_Count+1), width = 10, command = self.run_Results))
        self.Results_Buttons[self.Race_Count].grid(row = 0, column = self.Race_Count)
        [self.Results_Entries[self.Race_Count][rowplace].grid(row = rowplace+1, column = self.Race_Count) for rowplace in range(0,5)]



    # Method to disable self.Results_Entries boxes
    # DO NOT MODIFY!
    def disable_Results_Entries(self):
        self.Results_Buttons[self.Race_Count].destroy()
        self.Results_Buttons[self.Race_Count] = Button(self.frame_Results_Scrollbox_Display, text = "Race {}".format(self.Race_Count+1), width = 10, state = DISABLED)
        self.Results_Buttons[self.Race_Count].grid(row = 0, column = self.Race_Count)
        [entry.destroy() for entry in self.Results_Entries[self.Race_Count]]
        self.Results_Entries[self.Race_Count].clear()
        for rowplace in range(0,5):
            if self.Game_Over:
                self.Results_Entries[self.Race_Count].append(Entry(self.frame_Results_Scrollbox_Display, textvariable = self.Results[self.Race_Count][rowplace], width = 12, state = DISABLED, cursor = "arrow"))
                self.Results_Entries[self.Race_Count][rowplace].grid(row = rowplace+1, column = self.Race_Count)
            else:
                self.Results_Entries[self.Race_Count].append(Entry(self.frame_Results_Scrollbox_Display, textvariable = self.Results[self.Race_Count][rowplace], width = 12, bd = 0, state = DISABLED, cursor = "arrow"))
                self.Results_Entries[self.Race_Count][rowplace].grid(row = rowplace+1, column = self.Race_Count, padx = 2, pady = 2)



    # Method to run when a button object in self.Results_Buttons is pressed
    # DO NOT MODIFY!
    def run_Results(self):
        Results_List = [entry.get().lower() for entry in self.Results[self.Race_Count]]         # Get names from current entry boxes
        Results_List = self.remove_Blanks(Results_List)                                         # Remove blanks from Results_List
        if len(Results_List) == 0:                                                              # Check for existence of at least one horse
            self.print_Message("There must be at least one horse racing.")                      # If no horses listed, print message
        elif not (self.check_Valid_Horses(Results_List)):
            self.print_Message("At least one of these is not a horse. Check spelling, extra spaces, etc.")
        elif (1 < self.check_Duplicate_Horses(Results_List)):
            self.print_Message("A horse cannot race against itself.")
        else:
            self.disable_Results_Entries()
            Results_List = self.sort_Horses(Results_List)
            while len(Results_List)<5:
                Results_List.append("")
            [self.Results[self.Race_Count][i].set(Results_List[i]) for i in range(0,5)]
            self.create_Results_Entries()



    # Method to reset the Results frame
    # DO NOT MODIFY!
    def reset_Results(self):
        [entry.destroy() for entry in self.Results_Buttons]                         # Destroy buttons in self.Results_Buttons
        [[entry2.destroy() for entry2 in entry] for entry in self.Results_Entries]  # Destroy entry boxes in self.Results_Entries
        self.Results.clear()                                                        # Empty self.Results
        self.Results_Entries.clear()                                                # Empty self.Results_Entries
        self.Results_Buttons.clear()                                                # Empty self.Results_Buttons
        self.create_Results_Entries()                                               # Call self.create_Results_Entries method
        self.frame_Results_Scrollbox.xview_moveto(0)                                # Move scrollbar to the left



    # Method to determine the values to display in self.frame_Game_Stats
    def run_Game_Stats(self):
        fullstats = self.db_cursor.execute("""SELECT Win, Races FROM Stats ORDER BY Timestamp DESC;""").fetchall()
        self.Game_Stats[0].set(len(fullstats))                      # Set number of games played
        if len(fullstats)==0:                                       # If no games played, set other stats to 0
            for i in range(1,4):
                self.Game_Stats[i].set(0)
        else:                                                       # If game records exist:
            self.Game_Stats[1].set(sum([i[0] for i in fullstats]))  # Set total number of wins
            streak_Count = 0
            while ((streak_Count < len(fullstats)) and (fullstats[streak_Count][0] == fullstats[0][0])):
                streak_Count += 1
            self.Game_Stats[2].set((2*fullstats[0][0]-1)*streak_Count)
            fewest_Races = [0,0]
            for i in range(0,len(fullstats)):
                if (fullstats[i][0] == 1):
                    if (fewest_Races[0] == 0):
                        fewest_Races = [1,fullstats[i][1]]
                    else:
                        fewest_Races = min(fewest_Races,fullstats[i][1])
            self.Game_Stats[3].set(fewest_Races[1])



    # Method to run when "Reset Stats" button is pressed
    # DO NOT MODIFY!
    def reset_Stats(self):
        self.db_cursor.execute("""DELETE FROM Stats;""")    # Remove all entries from Stats table
        self.db_connection.commit()                         # Commit to database
        self.run_Game_Stats()                               # Get Game Stats
        if not self.Game_Over:                              # If in the middle of a game, add entry to Stats table
            self.db_cursor.executemany("""INSERT INTO Stats (Timestamp, Win, Races) VALUES (?,0,0)""",[(time(),)])
            self.db_connection.commit()



    # Method to run at start of game and when "New Game" button is pressed
    # DO NOT MODIFY!
    def new_Game(self):
        self.shuffle_Horses()                   # Shuffle the horses
        self.Game_Over = False                  # Set self.Game_Over to False
        self.reset_Results()                    # Reset self.Results_Entries boxes
        self.create_disabled_Guess_Entries()    # Create diabled self.Guess_Entries boxes
        self.enable_Guess_Entries()             # Enable self.Guess_Entries boxes
        self.run_Game_Stats()                   # Get game stats
        # Create new entry in Stats table (next two lines)
        self.db_cursor.executemany("""INSERT INTO Stats (Timestamp, Win, Races) VALUES (?,0,0)""",[(time(),)])
        self.db_connection.commit()
        self.print_Message("\nNew Game Started\n")



    # Method to print messages to self.Message_Text
    # DO NOT MODIFY!
    def print_Message(self, message):
        self.Messages_Text.config(state = NORMAL)
        self.Messages_Text.insert(END, "\n"+message)
        self.Messages_Text.config(state = DISABLED)
        self.Messages_Text.yview_moveto(1)



    # Method to shuffle the horses
    # DO NOT MODIFY!
    def shuffle_Horses(self):
        shuffle_List = [i for i in range(0,25)]
        for ep_Max in range(24,-1,-1):
            exchange_Position = randint(0,ep_Max)
            num_Temp = shuffle_List[exchange_Position]
            shuffle_List[exchange_Position] = shuffle_List[ep_Max]
            shuffle_List[ep_Max] = num_Temp
        self.Horse_Dictionary = {}
        for i in range(0,25):
            self.Horse_Dictionary[self.Horse_Names[shuffle_List[i]].lower()] = i
            self.Horse_Dictionary[str(i)] = self.Horse_Names[shuffle_List[i]]


    
    # Method to remove blank horse entries
    # DO NOT MODIFY!
    def remove_Blanks(self,Name_List):
        while (Name_List.count("") != 0):
            Name_List.remove("")
        return Name_List
    


    # Method to check for valid horse names
    # DO NOT MODIFY!
    def check_Valid_Horses(self,Name_List):
        Lower_Names = [name.lower() for name in self.Horse_Names]
        is_Valid = 1
        i = 0
        while ((i < len(Name_List)) and is_Valid):
            is_Valid = Lower_Names.count(Name_List[i])
            i += 1
        return is_Valid



    # Method to check for duplicate horse names
    # DO NOT MODIFY!
    def check_Duplicate_Horses(self,Name_List):
        return max([Name_List.count(name) for name in Name_List])



    # Method to sort horses
    # DO NOT MODIFY!
    def sort_Horses(self,Sort_List):
        for i in range(0,len(Sort_List)):
            Sort_List[i] = self.Horse_Dictionary[Sort_List[i]]
        Sort_List.sort()
        for i in range(0,len(Sort_List)):
            Sort_List[i] = self.Horse_Dictionary[str(Sort_List[i])]
        return Sort_List



    #
    # End of class
    #



def main():
    rootWindow = Tk()
    racetrack = Horses(rootWindow)
    rootWindow.mainloop()



if __name__ == "__main__": main()



'''
rootWindow = Tk()
racetrack = Horses(rootWindow)
'''

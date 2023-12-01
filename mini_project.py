from tkinter import filedialog as fdi

class character():
    def __init__(self, name):
        self.name = name

    #using to find where the character in map
    #return;[x,y]-->list
    def _findloc(self, locations):
        for i in range(len(locations)):
            for j in range(len(locations[i])):
                temp = locations[i][j]
                if type(temp) != int and temp.name == self.name:
                    return [i, j]
    #to move the character in maps
    def _move(self, locations, new_x, new_y):
        print('Start to Move')
        now_x, now_y = self._findloc(locations)
        locations[now_x][now_y], locations[new_x][new_y] = locations[new_x][new_y], locations[now_x][now_y]


class map():

    #initilize the map, contain(3police,1theif place in the position shows as document)
    #store each character's location in "all_location as dictionary"
    def __init__(self):
        # initilize the play characters
        print("loading the police")
        self.police_1 = character('A')
        self.police_2 = character('B')
        self.police_3 = character('C')

        print('Loading the theif')
        self.thief = character('T')
        # using 2D arry to represent the map
        self.locations = [[-1, self.thief, -1],
                          [0] * 3,
                          [0] * 3,
                          [self.police_1, self.police_2, self.police_3]
                          ]

        self.all_location = {'T': [], 'A': [], 'B': [], 'C': []}
        self._updateloca()

    # using to display the MAP
    def _shows_map(self):
        print('Map is loading:')
        count = ''
        for i in self.locations:
            for j in i:
                if type(j) == int:
                    count += str(j) + '        '
                else:
                    count += str(j.name) + '        '

            print(count)
            count = ''
    #using for update each character's location
    def _updateloca(self):
        self.all_location['T'] = self.thief._findloc(self.locations)
        self.all_location['A'] = self.police_1._findloc(self.locations)
        self.all_location['B'] = self.police_2._findloc(self.locations)
        self.all_location['C'] = self.police_3._findloc(self.locations)


class main():
    def __init__(self):
        #GameOver= 0 end the game
        self.GameOver = 1
        # 0 means the Police act, 1 means the thief act
        self.action = 0
        self.MAP = map()

    #run the game
    def _run(self):
        print('Game is started')

        while self.GameOver:
            self.name = ''
            self.new_x=0
            self.new_y=0

            self.MAP._shows_map()
            self._menue()
            if self.name == 'T':
                self.MAP.thief._move(self.MAP.locations, self.new_x, self.new_y)
            elif self.name == 'A':
                self.MAP.police_1._move(self.MAP.locations, self.new_x, self.new_y)
            elif self.name == 'C':
                self.MAP.police_3._move(self.MAP.locations, self.new_x, self.new_y)
            else:
                self.MAP.police_2._move(self.MAP.locations, self.new_x, self.new_y)
            self.MAP._updateloca()

            if self.action:
                self.action =0
            else:
                self.action=1
            self._checkgameover(self.name)

            #When GameOVER
            if not(self.GameOver):
                print("recording the result on doucment")
                with open('GameResult.txt','a+') as result:
                    result.write('This round Game\n')
                    for i in self.MAP.locations:
                        line = ''
                        for j in i:
                            if type(j) == int:
                                line += str(j) + ','
                            else:
                                line += j.name + ','
                        result.write(line + '\n')
                    result.write('winner is %s !!!'%self.winner)

    #display the operating menue
    def _menue(self):
        option = input('\nPleased Input(S)ave the game or (L)oad the game from file \n anything else for Start and continue the game with out file')
        option = str(option)

        if option =='S':
            print('save in the game file')
            self._savetheGame()
            return self._menue()

        elif option == 'L':
            print('Loading the Game')
            self._loadtheGame()
            return self._menue()
        else:
            if self.action:
                moving = input('Now is the round of Theif, pleased input as: (T),moveline,movecolumn  ; (split input by ",") ')

            else:
                moving = input('Now is the round of police, pleased choose an police input as: (A)/(B)/(C),line moving,column moving;(split input by ",")')

            print(self.MAP.all_location)
            self.name, self.new_x, self.new_y = moving.split(',')
            self.new_x, self.new_y = int(self.new_x) , int(self.new_y)

            if self._CheckMove(self.MAP.all_location, self.name,self.new_x,self.new_y):
                print('Input is Valid moving started')
            else:
                return self._menue()

    #check the move of character is valid
    def _CheckMove(self, allocation, name, x, y):
        print(self.action,name)
        if (self.action and name != 'T') or (not(self.action)and name=='T'):
            print('you are choose wrong characters, pleased choos again')
            return False
        
        elif 0 <= x <= 3 and 0 <= y <= 3:
            now_x, now_y = allocation[name]
            edge = self._findedge(now_x, now_y)

            if [x, y] in edge:
                return True
            else:
                print('u can move connected neighbor node and with out others police only')
                return False

        else:
            print('your column or line is out range')
            return False

    #using for find the position which character can move
    #give the character position in x,y
    def _findedge(self, x, y):
        edge = []
        #take information from locations
        for i in range(len(self.MAP.locations)):
            for j in range(len(self.MAP.locations[i])):

                #no -1 position
                if self.MAP.locations[i][j] != -1:
                    #cannot go the position already have Police
                    if type(self.MAP.locations[i][j])!= int:
                        if self.MAP.locations[i][j].name in 'ABC':
                            pass
                        else:
                            if i == x + 1 or i == x - 1 or (i == x and (j == y + 1 or j == y - 1)):
                                edge.append([i, j])
                    else:
                        if i == x + 1 or i == x - 1 or (i == x and (j == y + 1 or j == y - 1)):
                            edge.append([i, j])
        return edge

    def _checkgameover(self,name):
        self.winner= 0
        print('Checking the game over')
        print(self.MAP.all_location['T'][0])
        if self.MAP.all_location['T'][0]==3:
            self.winner = 'Thief'
            print('Game is Over The winner is %s!'%self.winner)
            self.GameOver =0
            return
        else:
            x,y = self.MAP.all_location['T']
            edge = self._findedge(x,y)
            if edge ==[]:
                self.winner='Police'
                print('Game is Over, there is no edge for Theif run out %s is winner'%self.winner)
                self.GameOver = 0
                return
        print('-----|------')
        print("continue")

    def _savetheGame(self):
        with open(input('plased input the file name for save')+'.txt','w+') as f:
            f.write(str(self.action)+'\n')
            for i in self.MAP.locations:
                line = ''
                for j in i:
                    if type(j)==int:
                        line+=str(j)+','
                    else:
                        line+=j.name+','

                f.write(line+'\n')

        print('Save complete')
 
    def _loadtheGame(self):
        file = fdi.askopenfilename(title='Pleased choose an file for loading',
                                   filetypes=[('TXT','.txt')],
                                   initialdir='./mini_project.py')
        with open(file,'r') as f:
            self.MAP.locations=[]
            lines=0
            self.action = int(f.readline().strip('\n'))

            for i in f.readlines():
                countline= i.split(',')[0:3]
                l = len(countline)
                for j in range(l):
                    temp = countline[j]
                    if temp =='0' or temp =='-1':
                        countline[j] = int(temp)
                    elif temp =='T':
                        countline[j]=self.MAP.thief
                    elif temp == 'A':
                        countline[j] = self.MAP.police_1
                    elif temp == 'B':
                        countline[j] = self.MAP.police_2
                    elif temp == 'C':
                        countline[j] = self.MAP.police_3
                print(countline)
                self.MAP.locations.append(countline)
            print('file is loading')
            self.MAP._updateloca()
            self.MAP._shows_map()

if __name__ == '__main__':
    main = main()
    main._run()

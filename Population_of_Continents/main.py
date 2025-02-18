import getData  # Importing all the content of the getData.py file
import pandas as pd


class Region:

    # The initialization of the parameters of the class Region
    def __init__(self, first_name="", second_name="", year=None, df_dict=None):
        self.first_name = first_name  # First region
        try:
            self.first_dataframe = df_dict[
                self.first_name]  # From the dictionary we choose the Dataframe with the region that we are interested in
        except KeyError:
            self.first_dataframe = ""
        self.second_name = second_name  # Second region name
        try:
            self.second_dataframe = df_dict[self.second_name]
        except KeyError:
            self.second_dataframe = ""
        self.year = year  # The year that we are interested in

    def display_population(self):
        return f"The population of the {self.first_name} is: {self.first_dataframe.loc[
            self.first_dataframe["Year"] == self.year, "Pop."].values[0]}"

    def population_comparison(self):
        # Compare the population of between two regions in a specific year.
        first_population = self.first_dataframe.loc[
            self.first_dataframe["Year"] == self.year, "Pop."].values[0]

        second_population = self.second_dataframe.loc[
            self.second_dataframe["Year"] == self.year, "Pop."].values[0]

        if first_population > second_population:
            return f"The population of {self.first_name} is larger than {self.second_name}"
        elif first_population < second_population:
            return f"The population of {self.second_name} is larger than {self.first_name}"
        else:
            return f"The population of {self.second_name} is equal with the population of {self.first_name}"

    def population_sort(self):
        # pop_list represents and intermediary step in order to create df that will be sorted based on population
        pop_list = [region_data_frames_dict[name].loc[
                        region_data_frames_dict[name]["Year"] == self.year, "Pop."].values[0] for name in
                    region_names]
        pop_df = pd.DataFrame({"Region": region_names, "Population": pop_list})
        return pop_df.sort_values(by="Population")
        # Needs to search in each region file for the specific year and take all data for each region population

    def growth_calculator(self):
        # Calculate the annual growth rate of a region in a specific year
        return f"The annual growth rate for the region of {self.first_name} is: {self.first_dataframe.loc[
            self.first_dataframe["Year"] == self.year, "±% p.a."].values[0]}"

    def growth_comparison(self):
        # Compares the growth rate between two regions in a specific year
        growth_first_region = self.first_dataframe.loc[
            self.first_dataframe["Year"] == self.year, "±% p.a."].values[0]
        growth_second_region = self.second_dataframe.loc[
            self.second_dataframe["Year"] == self.year, "±% p.a."].values[0]
        if growth_second_region != "—" or growth_first_region != "—":
            if growth_first_region > growth_second_region:
                return f"The growth rate of {self.first_name} is higher than the growth of the {self.second_name}"
            elif growth_first_region < growth_second_region:
                return f"The growth rate of {self.second_name} is higher than the growth of the {self.first_name}"
            else:
                return f"The growth rate of {self.second_name} is equal with the growth of the {self.first_name}"
        else:
            return f"The growth rate value of the {self.first_name} or {self.second_name} in the year {self.year} does not exist! "

    def growth_sort(self):
        # Sorts regions by growth rate in a specific year.
        growth_rate_list = [region_data_frames_dict[name].loc[
                                region_data_frames_dict[name]["Year"] == self.year, "±% p.a."].values[0] for name
                            in
                            region_names]
        growth_rate_df = pd.DataFrame({"Region": region_names, "±% p.a.": growth_rate_list})
        return growth_rate_df.sort_values(by="±% p.a.")


class Continent(Region):
    def __init__(self, first_name="", second_name="", year=None, df_dict=None):
        super().__init__(first_name, second_name, year, df_dict)

    def population_sort(self):
        # pop_list represents and intermediary step in order to create df that will be sorted based on population
        pop_list = [continental_data_frames_dict[name].loc[
                        continental_data_frames_dict[name]["Year"] == self.year, "Pop."].values[0] for name in
                    continental_names]
        pop_df = pd.DataFrame({"Continent": continental_names, "Population": pop_list})
        return pop_df.sort_values(by="Population")

    def growth_sort(self):
        # Sorts regions by growth rate in a specific year.
        growth_rate_list = [continental_data_frames_dict[name].loc[
                                continental_data_frames_dict[name]["Year"] == self.year, "±% p.a."].values[0] for name
                            in
                            continental_names]
        growth_rate_df = pd.DataFrame({"Continent": continental_names, "±% p.a.": growth_rate_list})
        return growth_rate_df.sort_values(by="±% p.a.")


# Creating two dictionary of dataframes using dictionary comprehension in order to have separate region dataframe from continental dataframe both in one single dictionary of Dataframes
region_data_frames_dict = {file: pd.read_csv(f"data/{file}.csv") for file in getData.list_table_names}
region_names = [name for name in getData.list_table_names if
                "Total" not in name]  # Splitting the Regions names from the imported list from the Continentals

continental_data_frames_dict = {file: pd.read_csv(f"data/{file}.csv") for file in getData.list_table_names}
continental_names = [name for name in getData.list_table_names if
                     "Total" in name]  # Splitting the Continents names from Regions


#################################################################################################################################

##### ///// #### The class Menu, handles all the errors, and different parts/bits of the code. Each Method do only a few things for
# easier understanding and esier debugging. Having the code i small parts also makes it easier for us to only call sepearte parts
# deping on the user input ##### ////// #####

class Menu:
    # Make the years to a string for easier display in the menu
    # Shared across all intances of the class
    years_int = [1950, 1960, 1970, 1980, 1990, 2000, 2010, 2021]
    years_str1 = " - ".join([str(year) for year in years_int])

    def __init__(self, region_names, continental_names):
        self.region_names = region_names
        self.continental_names = continental_names

    def region_or_continent(self):
        input_r_or_c = input("Please select 1 for Region or select 2 for the Continent: ")
        while True:
            if input_r_or_c not in ["1", "2"]:
                input_r_or_c = input(
                    "You didn't select 1 or 2 for the Region or Continent!\nPlease select 1 for Region or select 2 for the Continent: ")
            else:
                break
        return input_r_or_c

    def user_input_first_name(self, region_or_continent):
        input_user_f_name = input(self.display_num_and_region_or_continental(region_or_continent))
        while True:
            try:
                int(input_user_f_name)
            except ValueError:
                input_user_f_name = input(self.display_num_and_region_or_continental(region_or_continent))
            else:
                if region_or_continent == "1" and int(input_user_f_name) in range(len(region_names)):
                    return region_names[int(input_user_f_name)]
                elif region_or_continent == "2" and int(input_user_f_name) in range(len(continental_names)):
                    return continental_names[int(input_user_f_name)]
                else:
                    input_user_f_name = input(self.display_num_and_region_or_continental(region_or_continent))

    def user_input_second_name(self, region_or_continent):
        input_user_s_name = input(
            f"Please select the second {'Region' if region_or_continent == "1" else 'Continent'}: ")
        while True:
            try:
                int(input_user_s_name)
            except ValueError:
                input_user_s_name = input(self.display_num_and_region_or_continental(region_or_continent))
            else:
                if region_or_continent == "1" and int(input_user_s_name) in range(len(region_names)):
                    return region_names[int(input_user_s_name)]
                elif region_or_continent == "2" and int(input_user_s_name) in range(len(continental_names)):
                    return continental_names[int(input_user_s_name)]
                else:
                    input_user_s_name = input(self.display_num_and_region_or_continental(region_or_continent))

    def user_input_year(self):
        print(Menu.years_str1)
        year_prompt = input("Select a year from above: ")  # convert to interger
        while True:
            try:
                if int(year_prompt) not in Menu.years_int:
                    print(f"{year_prompt} is not in the list of allowed years. Please select a valid year.")
                    raise ValueError('Invalid input')
            except (ValueError, IndexError):
                year_prompt = input("Select a year from above: ")
            else:
                return int(year_prompt)

    def display_num_and_region_or_continental(self, region_or_continent):
        if region_or_continent == "1":
            for i in range(0, len(self.region_names)):
                print(i, self.region_names[i])
            return "Please select a Region: "
        else:
            for i in range(0, len(self.continental_names)):
                print(i, self.continental_names[i])
            return "Please select a Continent: "
        # design code for the menu


while True:

    menu_text = "Menu\n1. Display the population of a region or continent.\n2. Compare the population between two regions or continents\n3. Sort regions or continents by population size.\n4. Calculate the annual growth rate of region or continent.\n5. Compare the growth rate between two regions or continents\n6. Sort regions or continents by growth rate\n7. Exit\n"

    print(menu_text)
    user_input = input("Choose an option, by selecting a number from 1-7: ")


    def user_option(choose):
        match choose:
            case "1":
                menu = Menu(region_names, continental_names)
                if menu.region_or_continent() == "1":
                    region = Region(first_name=menu.user_input_first_name("1"), year=menu.user_input_year(),
                                    df_dict=region_data_frames_dict)
                    print(region.display_population())
                else:
                    continent = Continent(first_name=menu.user_input_first_name("2"), year=menu.user_input_year(),
                                          df_dict=continental_data_frames_dict)
                    print(continent.display_population())

            case "2":
                menu = Menu(region_names, continental_names)
                if menu.region_or_continent() == "1":
                    region = Region(menu.user_input_first_name("1"), menu.user_input_second_name("1"),
                                    menu.user_input_year(), region_data_frames_dict)
                    print(region.population_comparison())
                else:
                    continent = Continent(menu.user_input_first_name("2"), menu.user_input_second_name("2"),
                                          menu.user_input_year(), continental_data_frames_dict)
                    print(continent.population_comparison())
            case "3":
                menu = Menu(region_names, continental_names)
                if menu.region_or_continent() == "1":
                    region = Region(year=menu.user_input_year(), df_dict=region_data_frames_dict)
                    print(region.population_sort())
                else:
                    continent = Continent(year=menu.user_input_year(), df_dict=continental_data_frames_dict)
                    print(continent.population_sort())
            case "4":
                menu = Menu(region_names, continental_names)
                if menu.region_or_continent() == "1":
                    region = Region(first_name=menu.user_input_first_name("1"), year=menu.user_input_year(),
                                    df_dict=region_data_frames_dict)
                    print(region.growth_calculator())
                else:
                    continent = Continent(first_name=menu.user_input_first_name("2"), year=menu.user_input_year(),
                                          df_dict=continental_data_frames_dict)
                    print(continent.growth_calculator())

            case "5":
                menu = Menu(region_names, continental_names)
                if menu.region_or_continent() == "1":
                    region = Region(first_name=menu.user_input_first_name("1"),
                                    second_name=menu.user_input_second_name("1"), year=menu.user_input_year(),
                                    df_dict=region_data_frames_dict)
                    print(region.growth_comparison())
                else:
                    continent = Continent(first_name=menu.user_input_first_name("2"),
                                          second_name=menu.user_input_second_name("2"), year=menu.user_input_year(),
                                          df_dict=continental_data_frames_dict)
                    print(continent.growth_comparison())
            case "6":
                menu = Menu(region_names, continental_names)
                if menu.region_or_continent() == "1":
                    region = Region(year=menu.user_input_year(), df_dict=region_data_frames_dict)
                    print(region.growth_sort())
                else:
                    continent = Continent(year=menu.user_input_year(), df_dict=continental_data_frames_dict)
                    print(continent.growth_sort())
            case "7":
                print("exiting the program....")
                exit()
            case _:
                print("You didn't choose any of the options available from 1-7")


    user_option(user_input)

import gspread
import re
import functions as fct


# Metadata
version = "1.0.0"


# Load config files
config_path = "/Users/tylertran/Documents/projects/budgeting_link/config.yaml"
config = fct.read_yaml(config_path)
t_config = config["target"]
r_config = config["ref"]

# Connecting to worksheets
sa = gspread.service_account()
t = sa.open(t_config["book"])
t_wks = t.worksheet(t_config["sheet"])

r = sa.open(r_config["book"])
r_wks = r.worksheet(r_config["sheet"])


r_start = r_config["index"]
r_stop = fct.next_available_row(r_wks)
t_start = t_config["index"] + 1
t_stop = fct.next_available_row(t_wks)
ticks = r_stop - r_start

# Salutations message
fct.salutations(version)


# Loop runs X amount of times.
# X being the difference between the next empty row and the last filled row.
if ticks == 0:
    print("No new values to enter. Courier returning home.")

elif ticks > 0:
    for i in range(ticks):
        r_row = r_wks.row_values(r_start)
        print("\nTransferring data:", r_row)        #DEBUG


        involvement_check = r_row[6] == "1"

        input_date = fct.remove_whitespace(r_row[0])
        input_dollar = fct.remove_whitespace(r_row[8])
        input_dollar = fct.remove_special(input_dollar)


        if involvement_check:
            insert_values = [
                r_row[0],
                r_row[1],
                r_row[3],
                r_row[4],
                r_row[8]
            ]

            t_wks.insert_row(insert_values, index=t_start, value_input_option="USER_ENTERED")
            print("Insert success.")


        # Tick counter to update how many indices program has iterated through
        r_start += 1   
        t_start += 1
        #print("ref counter", r_start)       #DEBUG
        #print("target counter", t_start)    #DEBUG

    # Update config
    config["target"]["index"] = t_start
    config["ref"]["index"] = r_start

    try:
        fct.write_yaml(config, config_path)
    except:
        print("Writing to YAML failed.")

    # Good ending
    print(f"{ticks} entries transferred successfully. Courier returning home.")


else:
    print("Something went wrong. Courier got lost.")








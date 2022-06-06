import gspread
import re
import time
import functions as fct

import sys
import os

# Setup
cwd = os.path.dirname(os.path.realpath(__file__))
version = "1.0.0"
config_load = False

try: 
    # Load config files
    config_path = f"{cwd}/config.yaml"
    backup_config = f"{cwd}/backup.yaml"
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

    config_load = True
except KeyError:
    print("There was an error loading the configuration file.")
except FileNotFoundError:
    print("The configuration file was not found.")


def main():
    if config_load:
        # Salutations message
        fct.salutations(version)

        # Begin loop
        if ticks == 0:
            print("\nNo new values to enter. Courier returning home.")

        elif ticks > 0:
            insert_counter = 0
            print("\nData found. Beginning delivery process.\n")
            time.sleep(1)

            for i in range(ticks):
                r_row = r_wks.row_values(r_start)


                involvement_check = r_row[6] == "1"

                # Data cleansing
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

                    # Print data statement for debug
                    print("Data:", insert_values)

                    t_wks.insert_row(insert_values, index=t_start, value_input_option="USER_ENTERED")
                    print("Insert success.")

                    t_start += 1
                    insert_counter += 1


                r_start += 1       



            # Config backup handling
            try:
                fct.write_yaml(config, backup_config)
            except:
                print("\n Backup failed.")

            # Config updating
            config["target"]["index"] = t_start
            config["ref"]["index"] = r_start

            try:
                fct.write_yaml(config, config_path)
            except:
                print("\nWriting to YAML failed.")

            # Good ending
            print(f"\n{insert_counter} entries transferred successfully. Courier returning home.\n")


        else:
            print("\nSomething went wrong. Courier got lost.\n")

    else:
        print("\nConfiguration was not loaded. Courier going home.\n")


if __name__ == "__main__":
    main()


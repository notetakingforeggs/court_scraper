def user_interface():
    """Handles user interaction and flow control."""
    session = login()
    if not session:
        return

    while True:
        option = input("Check all courts or one court? (all/one/exit): ").strip().lower()
        
        if option == "all":
            # get links
            court_links = get_court_links(session)
            if not court_links:
                print("No court links found.")
            else:
                # search within links for keyword
                search_cases(session, court_links)

        elif option == "one":
            courts = get_court_list(session)
            if not courts:
                print("No courts available.")
                continue

            court_name = input("Enter the court name: ").strip()
            court = search_court_by_name(court_name, courts)
            
            if court:
                search_names_in_court(session, court)
            else:
                print("Court not found. Available courts:")
                list_courts(courts)

        elif option == "exit":
            print("Exiting...")
            break

        else:
            print("Invalid option. Please choose 'all', 'one', or 'exit'.")
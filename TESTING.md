
## Manual Testing

### Site Navigation

| **Element**           | **Action** | **Expected Result**                                                | **Pass/Fail** |
|-----------------------|------------|--------------------------------------------------------------------|---------------|
| **Navbar**            |            |                                                                    |               |
| Site Name (logo area) | Click      | Redirect to home                                                   | Pass          |
| Home Link             | Click      | Redirect to home                                                   | Pass          |
| Browse Recipes Link   | Click      | Open Browse Recipes Page                                           | Pass          |
| Add Recipe Link       | Click      | Open Add Recipe Form                                               | Pass          |
| Add Recipe Link       | Display    | Only visble if user in session                                     | Pass          |
| My Meal Plan Link     | Click      | Open My Meal Plan page                                             | Pass          |
| My Meal Plan Link     | Display    | Only visble if user in session                                     | Pass          |
| My Account Dropdown   | Click      | Open My Account dropdown                                           | Pass          |
| My Account Dropdown   | Display    | Text changes to username with profile icon when user is in session | Pass          |
| Sign Up Link          | Click      | Open Sign up page                                                  | Pass          |
| Sign Up Link          | Display    | Not visible if user in session                                     | Pass          |
| Log In Link           | Click      | Open Log in page                                                   | Pass          |
| Log In Link           | Display    | Not visible if user in session                                     | Pass          |
| My Recipes Link       | Click      | Open My Recipes page                                               | Pass          |
| My Recipes Link       | Display    | Only visible if user in session                                    | Pass          |
| My Bookmarks Link     | Click      | Open My Bookmarks page                                             | Pass          |
| My Bookmarks Link     | Display    | Only visible if user in session                                    | Pass          |
| Logout Link           | Click      | Open logout confirm page                                           | Pass          |
| Logout Link           | Display    | Only visible if user in session                                    | Pass          |
| All Nav Links         | Hover      | Darken text                                                        | Pass          |
| All Nav Links         | If active  | Keep active link dark and bold                                     | Pass          |
| Navbar                | Scroll     | Remains fixed to top of page                                       | Pass          |

### Home Page

### Browse Recipes Page
### Recipe Detail Page
### Add Recipe Page
### Edit Recipe Page
### Confirm Delete Recipe Page
### My Recipes Page
### My Bookmarks Page
### My Meal Plan Page
### Django All Auth Pages
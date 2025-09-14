# Project Progress

### Core Features (From Proposal)

- [x] **User Authentication & Profiles**
  - [x] User registration
  - [x] User login
  - [x] User profiles
  - [x] Profile editing (username, email, bio)
- [x] **Post Functionality**
  - [x] Create new posts
  - [x] Share posts
  - [x] Edit existing posts
  - [x] Delete posts
- [x] **Social Interactions**
  - [x] Add reactions to posts
  - [x] Add comments to posts
  - [x] Follow and unfollow users
- [x] **Homepage & Feed**
  - [ ] Homepage to display a feed of posts
  - [x] Display posts from followed users
  - [x] Post reaction counters
  - [x] Post comment section

***

### Features Added During Development 

These features were not part of the original proposal but have been implemented to improve the project.

- **Post Image Management**
  - [x] Allow post creation without a required image
  - [x] Allow authors to remove an image from a post when editing
- **Post Visibility**
  - [x] Re-add the post visibility feature (public or followers-only)
- **Shared Posts**
  - [x] Add a share post feature
- **Post Detail Page**
  - [x] Create a dedicated post detail page for each post

***

### Concurrent Bugs & Known Issues

- **Homepage & Feed**
  - The homepage feed is not correctly filtering posts based on their visibility.
  - The "shared post" does not indicate it is a shared post.


- **Post Reaction Counters**
  - The reaction counters may display an incorrect count of zero due to an inefficient database query.
 

- **Share Button**
  - The homepage feed does not display the share button and prompt but it displays properly when viewed in the profile. 

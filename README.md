## Project Progress Tracker 🚀

This is a progress tracker to help you manage the development of your social media project. It lists the core features from your proposal, new features we've added, and a list of known bugs.

### Core Features (From Proposal)

- [ ] **User Authentication & Profiles**
  - [x] User registration
  - [x] User login
  - [x] User profiles
  - [x] Profile editing (username, email, bio)
- [ ] **Post Functionality**
  - [x] Create new posts
  - [x] Edit existing posts
  - [x] Delete posts
- [ ] **Social Interactions**
  - [x] Add reactions to posts
  - [x] Add comments to posts
  - [x] Follow and unfollow users
- [ ] **Homepage & Feed**
  - [ ] Homepage to display a feed of posts
  - [x] Display posts from followed users
  - [ ] Post reaction counters
  - [x] Post comment section

***

### Features Added During Development ✨

These features were not part of the original proposal but have been implemented to improve the project.

- **Post Image Management**
  - [x] Allow post creation without a required image
  - [x] Allow authors to remove an image from a post when editing

***

### Concurrent Bugs & Known Issues 🐛

This is a list of known bugs that we have decided to set aside for now but need to be addressed in the future.

- **Homepage Post Visibility:** The `post_list` function on the homepage currently does not filter to include the current user's own posts, only posts from followed users.
- **Reaction Counters:** The reaction counters on the homepage are not always working correctly and may display a count of `0` even when a post has reactions. This is due to an inefficient database query.
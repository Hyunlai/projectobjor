### **Changelog**

This is a log of all the changes as of 9/17/2025 to the Chinguloop project.

#### **Version 1.1**

**New Features**

* **Detailed Post View:** Users can now click on a post to see a dedicated, detailed view with all comments and reactions.
* **Admin Dashboard Enhancements:**
    * A button to the Admin Dashboard is now visible on the navigation bar for all authenticated admins.
    * An "ADMIN" badge now appears next to the usernames of admins on both the post feed and the detailed post view, but only when another admin is logged in.

**Bug Fixes**

* **Fixed User Registration Bug:** The `FileNotFoundError` preventing new users from registering has been resolved. The image resizing logic was moved from the `save()` method in the `Profile` model to the `profile_update` view, ensuring it only runs after a profile picture has been explicitly uploaded.
* **Corrected Ban Button Logic:** The "Ban" button in the Admin Dashboard is now correctly hidden for posts made by other administrators.
* **`gitignore` Update:** The `.gitignore` file has been updated to track the `media/default/` folder and its contents, while still ignoring all other user-uploaded media files.

---

#### **Version 1.2**

**New Features**

* **Move Post Reactions:** The expandable "View Reactions" section was moved from the main home page to the detailed post view to reduce clutter.
* **Filterable Reactions:** On the detailed post view, users can now filter reactions by type (e.g., Like, Love, Haha) using new clickable buttons.
* **Comment Deletion:** Users can now delete their own comments and replies. Delete buttons are visible only to the comment's author.
* **Post Visibility Update:** The backend now includes a new `update_post_visibility` view and URL to handle changing a post's visibility (e.g., Public, Private) without having to edit the entire post.

**Removed Features**

* **Post Editing:** The ability to edit a post was removed, and the `edit_post` URL path was deleted.
Iteration 1
- Assume user is logged in upon registration: (is_success = False)

- Assume token given to auth_logout is a valid token (the person logging themself out gives their own token), and we don't have to test the token against certain things..

- Assume token is validated when attempting to create channels, or list channels

- Only global owners can channel_join private channels
Otherwise, only a person who is invited to a channel can join the private channel

- A user who makes a channel should immediately be added to the channel

-Global owner is 'us'
A person can only become an owner of a channel if they are a member

-Need to remove ownership if a person leaves a channel
the global owner is the owner of (the) flockr, and gain the same permissions as a owner_member upon joining a channel, regardless of whether its private or not, but do not explicitly become owner_members

- in the scenario that the global owner is also an owner_member of a channel, can the remove_owner operation still apply to the global owner?
    -Yes, since either being an owner or being a global user allows users to add or remove owners. 

- If the last user leaves a chanel, should the channel be automatically removed?
    - In the spec, it does not say to remove channel if last user leaves. For now the channel remains and user who has is_global activated can use addowner and channel_join (if channel is private) to restore users back into the empty channel

-A​​​​​​s of this moment, we are allowing multiple logins. It does not matter in our Iteration 1, because token is always set to email. 


Iteration 2 assumptions:

- Messages function limits message size to 1000 characters; ignore this fact in search since it's not being tested (piazza)

- Don't consider the join date of the user to the channel when searching messages: search through all messages even ones before the given user was part of the channel.

- first name and last name must be in between 1 and 50 characters. first name and last name Characters cannot be 1 or 50

- The u_id in user_profile can either be the user or a different user

- Assume every message, deleted or not, has a unique id.

- user can't change their own permissions

Iteration 3 assumptions:
- neglect some security issues of having multiple reset codes in data structure at once (when resetting password)

- standup/send uses a combination of sendlater and message edit

- The timestamp is an integer. The bigger the number the more into the future it is. The smaller the number the more into the past.

- Standup/send does not need to check if message is over 1000 characters

- Functions with get route may pass integers as strings

- Added try and except to check if img_url is valid

- Messages need to be sorted by time_created before returning it in channel_messages and search


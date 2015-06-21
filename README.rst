==============
 fingerchange
==============

``fingerchange`` is a simple gateway that lets you look up user profiles on StackExchange website using finger protocol clients.

Queries should be in the format of ``user@site`` where user is either a UID or a display name, and site is the domain of the StackExchange site you're fetching the user details from.
Doing a ``/W`` query will also fetch the ``about_me`` field.


Example
=======

Example output with ``/W``::

    === 425023 =====================================================================
     :: uid 33521
     :: name kyrias
     :: reputation 1113
     :: location Stockholm, Sweden
     :: profile <http://unix.stackexchange.com/users/33521/kyrias>
     :: website <https://theos.kyriasis.com/~kyrias>
     :: reputation changes
       :: quarter +320
       :: year +333

    --- About User -----------------------------------------------------------------

      Hey there, I'm just a crazy guy from Sweden who likes to play with
      various interesting software and technologies.

      You can contact me either through email at johannes@kyriasis.com, on
      IRC where I most often go by demize  and am most active on freenode,
      or (rarely) as kyrias@kyriasis.com on gale.

      If you for some reason would like to contact me more privately, my PGP
      key is 5134 EF9E AF65 F95B 6BB1  608E 50FB 9B27 3A9D 0BB5

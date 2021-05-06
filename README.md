# human-resource-management-system

this is a highly customized django project with the following functionalities available:

- This project is one of the most complete examples of Django translation projects available
  Because it has some hacks to translate `permissions` visible on the `django-admin` page. (This was a big deal, because you will not find a similar example out there!)
  There were some `flaws` in the default django `translation files for Persian` and `I fixed` them.

- A system to prevent repeated attempts to log in.

- A system for monitoring `password changes` and `prevent` reuse of a password or a similar one, at least `4 characters` must be different.

- A system for `expiring passwords` after `specified period` of time.

- A `customized log-entry` system.

- A `reporting` system for required sections directly from `inside the admin panel`.

- Limit the `admin ListView items` with regard the `request.user`.

- Customized `login page` for django admin panel with `captcha`.

- Customized `change password view` for django admin panel.

- Customized `user` model with more fields and functions.

- A system to expire `session` after `specified period` of time.

- A `signal`-based system to kill all previous `sessions` after a new `session` has been setted.

- Good example of custom middlewares in django, e.g: `LoginRequiredMiddleware`, `PasswordValidationMiddleware` , ...

- Good use of `django-jalali-date` 3rd parity package by [Arman Roomana/a-roomana](https://github.com/a-roomana/django-jalali-date).

and a lot more functionalities that are beyond the scope of explanation.

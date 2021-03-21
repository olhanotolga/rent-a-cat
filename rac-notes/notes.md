# Notes & links

## Tools

- Canvas: https://canvas.instructure.com/courses/2484948
- Trello: https://trello.com/b/FeD124md/frauenloop-project-overview
- DB design (LucidChart): https://lucid.app/lucidchart/30bbb18a-24fd-4558-a4ff-6d3d4de1f350/edit?beaconFlowId=DE339A8875D1FF58&page=0_0#?folder_id=home&browser=icon
- Pages structure/flow: https://app.diagrams.net/#G1Kw74Ktoc5xltkEwirTzyQG6vq0xePCya
- GitHub repo: https://github.com/olhanotolga/rent-a-cat
- Figma: https://www.figma.com/files/project/14664758/Rent-a-Cat

## Stack

- Flask — the main thing
- WTForms — forms
- SQLAlchemy — the database

- Google Maps API
- SpatiaLite (store spatial data is SQLite and manipulate them, e.g. search by distance)
- GeoAlchemy (allows using spatial data with SQLAlchemy)

## Ideas

— little cat paws for likes/favorites

### Ideas for future

- many-to-many relationship between requests and offers with one of three possible statuses

## Problems

Could not figure out how to render a form label with a nested link.

1. Is it possible with `wtforms`?
2. Does it make sense from the accessibility point?
3. Is there a better way to solve it other than with an asterisk?

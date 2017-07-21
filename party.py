"""Flask site for Balloonicorn's Party."""

from flask import Flask, session, render_template, request, flash, redirect
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.secret_key = "SECRETSECRETSECRET"


def is_mel(name, email):
    """Is this user Mel?

        >>> is_mel('Mel Melitpolski', 'mel@ubermelon.com')
        True

        >>> is_mel('Judith Butler', 'judith@awesome.com')
        False

        >>> is_mel('Mel Melitpolski', '')
        True

        >>> is_mel('', 'mel@ubermelon.com')
        True

        >>> is_mel('', 'MEL@UBERMELON.COM')
        True

        >>> is_mel('mel', '')
        True

        >>> is_mel('Mel', '')
        True

        >>> is_mel('meL MeLiTpOlSkI', '')
        True

    """
    name = name.lower()    
    names = name.split(" ")

    is_mel = False
    if names[0] == "mel":
        is_mel = True

    if len(names) > 1 and names[0] == "mel":
        if names[1] == "melitpolski":
            is_mel = True

    email = email.lower()
    if email == 'mel@ubermelon.com':
        is_mel = True

    if is_mel:
        return True
    else:
        return False




def most_and_least_common_type(treats):
    """Given list of treats, return lists of most and least common treat types.

    Return most and least common treat types in tuple of format (most, least).

        >>> treats = [
        ...     {'type': 'drink'},
        ...     {'type': 'drink'},
        ...     {'type': 'drink'},
        ...     {'type': 'drink'},
        ...     {'type': 'drink'},
        ...     {'type': 'appetizer'},
        ...     {'type': 'appetizer'},
        ...     {'type': 'dessert'},
        ... ]

        >>> most_and_least_common_type(treats)
        (['drink'], ['dessert'])

        >>> treats = [
        ...     {'type': 'drink'},
        ...     {'type': 'drink'},
        ...     {'type': 'drink'},
        ...     {'type': 'drink'},
        ...     {'type': 'drink'},
        ...     {'type': 'appetizer'},
        ...     {'type': 'dessert'},
        ... ]
        >>> most_and_least_common_type(treats)
        (['drink'], ['appetizer', 'dessert'])
        

        >>> treats = [
        ...     {'type': 'drink'},
        ...     {'type': 'drink'},
        ...     {'type': 'drink'},
        ...     {'type': 'drink'},
        ...     {'type': 'drink'},
        ...     {'type': 'drink'},
        ...     {'type': 'drink'},
        ... ]

        >>> most_and_least_common_type(treats)
        (['drink'], ['drink'])

    """

    types = {}

    # Count number of each type
    for treat in treats:
        types[treat['type']] = types.get(treat['type'], 0) + 1

    most_type = []
    least_type = []

    #convert dict of treats into list and sort on count
    all_foods = list(types.items())
    all_foods.sort(cmp = lambda x,y: cmp(x[1],y[1]), reverse = True)

    #loop through sorted list and include all of the highest counts that match
    for i in range(len(all_foods)):
        if all_foods[i][1] == all_foods[0][1]:
            most_type.append(all_foods[i][0])
        else:
            break

    # loop through sorted list backwards and 
    # include all of the lowest counts that match
    for k in range(len(all_foods)-1, -1, -1):
        if all_foods[k][1] == all_foods[-1][1]:
            least_type.append(all_foods[k][0])
        else:
            break

    #returns list of most common and least common treats
    return (most_type, least_type)


def get_treats():
    """Return treats being brought to the party.

    One day, I'll move this into a database! -- Balloonicorn

    """

    return [
        {'type': 'dessert',
         'description': 'Chocolate mousse',
         'who': 'Leslie'},
        {'type': 'dessert',
         'description': 'Cardamom-Pear pie',
         'who': 'Joel'},
        {'type': 'appetizer',
         'description': 'Humboldt Fog cheese',
         'who': 'Meggie'},
        {'type': 'dessert',
         'description': 'Lemon bars',
         'who': 'Bonnie'},
        {'type': 'appetizer',
         'description': 'Mini-enchiladas',
         'who': 'Katie'},
        {'type': 'drink',
         'description': 'Sangria',
         'who': 'Anges'},
        {'type': 'dessert',
         'description': 'Chocolate-raisin cookies',
         'who': 'Henry'},
        {'type': 'dessert',
         'description': 'Brownies',
         'who': 'Sarah'}
    ]


@app.route("/")
def homepage():
    """Show homepage."""

    return render_template("homepage.html")


@app.route("/treats")
def show_treats():
    """Show treats people are bringing."""

    treats = get_treats()

    most, least = most_and_least_common_type(get_treats())

    return render_template("treats.html",
                           treats=treats,
                           most=most,
                           least=least)


@app.route("/rsvp", methods=['POST'])
def rsvp():
    """Register for the party."""

    name = request.form.get("name")
    email = request.form.get("email")

    if not is_mel(name, email):
        session['rsvp'] = True
        flash("Yay!")
        return redirect("/")

    else:
        flash("Sorry, Mel. This is kind of awkward.")
        return redirect("/")


if __name__ == "__main__":
    app.debug = True
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
    DebugToolbarExtension(app)
    app.run()

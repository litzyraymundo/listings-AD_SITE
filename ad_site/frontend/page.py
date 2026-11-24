from html import escape
from urllib.parse import quote, urlencode




COAT_IMAGE = "item-2.jpg"
CAMERA_IMAGE = "item-3.jpg"
BACKPACK_IMAGE = "item-4.jpg"


IMAGE_NAMES = {COAT_IMAGE, CAMERA_IMAGE, BACKPACK_IMAGE}
PREVIEW_LINK = "/?show=preview#how-it-works"


CATEGORIES = (
   ("all", "All listings"),
   ("sale", "For sale"),
   ("trade", "Trades"),
   ("free", "Free"),
)


CATEGORY_KEYS = {key for key, _ in CATEGORIES}
CATEGORY_BADGES = {"sale": "For sale", "trade": "Trade", "free": "Free"}


SAMPLE_LISTINGS = (
   (COAT_IMAGE, "Workwear Chore Coat", "$85", "sale", "/coat"),
   (CAMERA_IMAGE, "Compact Camera", "$65", "sale", None),
   (BACKPACK_IMAGE, "Canvas Daypack", "", "trade", None),
)


STYLES = """
* { box-sizing: border-box; }


body {
   margin: 0;
   background: #fcfaf3;
   color: #171714;
   font: 1rem/1.5 system-ui, sans-serif;
}


header, main {
   width: min(70rem, calc(100% - 2rem));
   margin-inline: auto;
}


header { padding-block: 1rem; }
main { padding-bottom: 2rem; }
a { color: inherit; }


.brand {
   font-size: 2rem;
   font-weight: 900;
   letter-spacing: -.08em;
   text-decoration: none;
}


.brand span { color: #ffd71c; }


.hero {
   padding: clamp(1.5rem, 6vw, 4rem);
   background: #ffd71c;
   border-radius: 1.75rem;
}


.hero h1 {
   margin: 0;
   font-size: clamp(2.75rem, 8vw, 6rem);
   line-height: 1;
   letter-spacing: -.07em;
}


.hero p:first-child { margin-top: 0; }


.button {
   display: inline-block;
   padding: .75rem 1.1rem;
   border: 0;
   border-radius: 999px;
   background: #171714;
   color: white;
   font: inherit;
   font-weight: 750;
   text-decoration: none;
   cursor: pointer;
}


:focus-visible {
   outline: 3px solid #171714;
   outline-offset: 3px;
}


section + section { margin-top: 2.5rem; }


.steps, .listing-grid, .item-detail {
   display: grid;
   gap: 1.25rem;
}


.steps {
   grid-template-columns: repeat(2, minmax(0, 1fr));
   padding-left: 1.4rem;
}


.steps > li:first-child { grid-column: 1 / -1; }
.steps strong { display: block; }


.listing-search {
   display: flex;
   align-items: center;
   gap: .25rem;
   max-width: 40rem;
   margin-top: .75rem;
   padding: .3rem;
   border: 1px solid #dedacf;
   border-radius: 999px;
   background: white;
}


.listing-search input[type="search"] {
   flex: 1 1 0;
   min-width: 0;
   padding: .65rem .8rem;
   border: 0;
   border-radius: 999px;
   background: transparent;
   font: inherit;
}


.listing-search button { flex: 0 0 auto; }


.category-filters {
   display: flex;
   flex-wrap: wrap;
   gap: .5rem;
   margin-top: .75rem;
}


.category-filters a {
   padding: .5rem .9rem;
   border: 1px solid #dedacf;
   border-radius: 999px;
   background: white;
   font-weight: 750;
   text-decoration: none;
}


.category-filters a[aria-current="true"] {
   border-color: #171714;
   background: #171714;
   color: white;
}


.listing-grid {
   grid-template-columns: repeat(3, minmax(0, 1fr));
}


figure { margin: 0; }


img {
   display: block;
   width: 100%;
   aspect-ratio: 4 / 3;
   object-fit: cover;
   border-radius: 1rem;
}


.listing-photo { position: relative; }
.listing-photo a { display: block; border-radius: 1rem; }


.listing-badge {
   position: absolute;
   top: .75rem;
   left: .75rem;
   padding: .35rem .7rem;
   border-radius: 999px;
   background: #ffd71c;
   font-weight: 750;
   pointer-events: none;
}


figcaption { margin-top: .6rem; }
figcaption span { display: block; }


.item-detail {
   grid-template-columns: repeat(2, minmax(0, 1fr));
   align-items: start;
}


.back-link {
   display: inline-block;
   margin-bottom: 1rem;
}


@media (max-width: 640px) {
   .steps, .listing-grid, .item-detail {
       grid-template-columns: 1fr;
   }
}
"""




def photo(filename, description, lazy=False):
   url = "/images/" + quote(filename, safe="")
   loading = ' loading="lazy"' if lazy else ""
   return f'<img src="{url}" alt="{escape(description)}"{loading}>'




def document(title, content):
   return f"""<!doctype html>
<html lang="en">
<head>
 <meta charset="utf-8">
 <meta name="viewport" content="width=device-width, initial-scale=1">
 <title>{escape(title)} | Listings</title>
 <style>{STYLES}</style>
</head>
<body>
 <header>
   <a class="brand" href="/">listings<span aria-hidden="true">●</span></a>
 </header>
 <main>
   {content}
 </main>
</body>
</html>
"""




def render_listing(filename, title, price, category, link):
   name = escape(title)
   picture = photo(filename, title, lazy=True)
   badge = CATEGORY_BADGES[category]
   price_line = f"<span>{escape(price)}</span>" if price else ""


   if link:
       picture = f'<a href="{link}" aria-label="View {name}">{picture}</a>'
       name = f'<a href="{link}">{name}</a>'


   return f"""
     <figure>
       <div class="listing-photo">
         {picture}
         <span class="listing-badge">{badge}</span>
       </div>
       <figcaption>
         <strong>{name}</strong>
         {price_line}
       </figcaption>
     </figure>
"""




def render_category_filters(query, category):
   links = []


   for key, label in CATEGORIES:
       params = urlencode({"show": "preview", "q": query, "category": key})
       href = escape(f"/?{params}#fresh-finds")
       current = ' aria-current="true"' if key == category else ""
       links.append(f'<a href="{href}"{current}>{label}</a>')


   return "\n".join(links)




def render_preview(query="", category="all"):
   words = query.casefold().split()
   cards = []


   for filename, title, price, item_category, link in SAMPLE_LISTINGS:
       if category != "all" and category != item_category:
           continue


       badge = CATEGORY_BADGES[item_category]
       searchable_text = f"{title} {badge} {price}".casefold()


       if all(word in searchable_text for word in words):
           cards.append(render_listing(filename, title, price, item_category, link))


   if cards:
       results = '<div class="listing-grid">' + "".join(cards) + "</div>"
   else:
       results = '<p role="status">No sample listings match these filters.</p>'


   filters = render_category_filters(query, category)


   return f"""
   <section id="Simple-and-easy">
     <h2>Simple and easy</h2>


     <ol class="steps">
       <li>
         <strong>Find an item.</strong>
         Browse items listed for sale, trade, or giveaway through the search bar, filters, or main page.


         <form class="listing-search" action="/#fresh-finds"
               method="get" role="search">
           <input type="hidden" name="show" value="preview">
           <input type="hidden" name="category" value="{escape(category)}">
           <input type="search" name="q" placeholder="Search listings"
                  aria-label="Search sample listings" maxlength="80"
                  value="{escape(query)}">
           <button class="button" type="submit">Search</button>
         </form>


         <nav class="category-filters" aria-label="Filter listings by type">
           {filters}
         </nav>
       </li>


       <li>
         <strong>Check the details.</strong>
         Read the description and condition of the item.
       </li>


       <li>
         <strong>Plan a meetup.</strong>
         Pick a date, time, and meeting spot on campus. Contact the seller separately
         to confirm.
       </li>
     </ol>
   </section>


   <section id="fresh-finds" aria-labelledby="fresh-finds-title">
     <h2 id="fresh-finds-title">Fresh finds</h2>
     <p>Sample listings from the marketplace.</p>
     {results}
   </section>
"""




def render_home(show_preview=False, query="", category="all"):
   preview = render_preview(query, category) if show_preview else ""


   return document("The college marketplace", f"""
   <section class="hero" aria-labelledby="headline">
     <p>The college marketplace.</p>
     <h1 id="headline">Find it. Meet up. Done.</h1>
     <p>Buy, trade, and give things away in person.</p>
     <a class="button" href="{PREVIEW_LINK}">See how it works</a>
   </section>


   {preview}
""")




def render_coat():
   return document("Workwear Chore Coat", f"""
   <a class="back-link" href="/">Back to main page</a>


   <div class="item-detail">
     {photo(COAT_IMAGE, "Rust-colored workwear coat")}


     <div>
       <p>Sample listing</p>
       <h1>Workwear Chore Coat</h1>
       <p><strong>$85</strong> · For sale · Good condition</p>
       <p>(Example description) A rust-colored workwear coat with a button front and roomy patch pockets.</p>


       <h2>Example meetup plan</h2>
       <p><strong>Saturday at 10:00 a.m.</strong> · Corner café</p>
       <p>(Contact the seller separately to confirm the time and place.)</p>
     </div>
   </div>
""")

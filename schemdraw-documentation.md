Schemdraw documentation[¶](#schemdraw-documentation "Link to this heading")
===========================================================================

Schemdraw is a Python package for producing high-quality electrical circuit schematic diagrams. Circuit elements are added, one at a time, similar to how you might draw them by hand, using Python methods.

For example,

with schemdraw.Drawing() as d:
    d += elm.Resistor().right().label('1Ω')

creates a new schemdraw drawing with a resistor going to the right with a label of “1Ω”. The next element added to the drawing will start at the endpoint of the resistor.

with schemdraw.Drawing() as d:
    d += elm.Resistor().right().label('1Ω')
    d += elm.Capacitor().down().label('10μF')
    d += elm.Line().left()
    d += elm.SourceSin().up().label('10V')

![_images/index_1_0.svg](_images/index_1_0.svg)

  

Getting Started[¶](#getting-started "Link to this heading")
-----------------------------------------------------------

### Installation[¶](#installation "Link to this heading")

schemdraw can be installed from pip using

pip install schemdraw

or to include optional `matplotlib` backend dependencies:

pip install schemdraw\[matplotlib\]

To allow the SVG drawing [Backends](index.html#backends) to render math expressions, install the optional [ziamath](https://ziamath.readthedocs.io) dependency with:

pip install schemdraw\[svgmath\]

Alternatively, schemdraw can be installed directly by downloading the source and running

pip install ./

Schemdraw requires Python 3.8 or higher.

### Overview[¶](#overview "Link to this heading")

The `schemdraw` module allows for drawing circuit elements. `schemdraw.elements` contains [Basic Elements](index.html#electrical) pre-defined for use in a drawing. A common import structure is:

import schemdraw
import schemdraw.elements as elm

To make a circuit diagram, a [`schemdraw.Drawing`](index.html#schemdraw.Drawing "schemdraw.Drawing") is created and [`schemdraw.elements.Element`](index.html#schemdraw.elements.Element "schemdraw.elements.Element") instances are added to it:

with schemdraw.Drawing() as d:
    d.add(elm.Resistor())
    d.add(elm.Capacitor())
    d.add(elm.Diode())

![_images/start_1_0.svg](_images/start_1_0.svg)

The += operator may be used as shorthand notation to add elements to the drawing. This code is equivalent to the above:

with schemdraw.Drawing() as d:
    d += elm.Resistor()
    d += elm.Capacitor()
    d += elm.Diode()

Element placement and other properties and are set using a chained method interface, for example:

with schemdraw.Drawing() as d:
    d += elm.Resistor().label('100KΩ')
    d += elm.Capacitor().down().label('0.1μF', loc\='bottom')
    d += elm.Line().left()
    d += elm.Ground()
    d += elm.SourceV().up().label('10V')

![_images/start_2_0.svg](_images/start_2_0.svg)

Methods up, down, left, right specify the drawing direction, and label adds text to the element. If not specified, elements reuse the same direction from the previous element, and begin where the previous element ended.

Using the with context manager is a convenience, letting the drawing be displayed and saved upon exiting the with block. Schematics may also be created simply by assinging a new Drawing instance, but this requires calling draw() and/or save() explicitly:

d \= schemdraw.Drawing()
d += elm.Resistor()
...
d.draw()
d.save('my\_circuit.svg')

For full details of placing and stylizing elements, see [Placing Elements](index.html#placement). and [`schemdraw.elements.Element`](index.html#schemdraw.elements.Element "schemdraw.elements.Element").

In general, parameters that control **what** is drawn are passed to the element itself, and parameters that control **how** things are drawn are set using chained Element methods. For example, to make a polarized Capacitor, pass polar=True as an argument to Capacitor, but to change the Capacitor’s color, use the .color() method: elm.Capacitor(polar=True).color(‘red’).

### Viewing the Drawing[¶](#viewing-the-drawing "Link to this heading")

#### Jupyter[¶](#jupyter "Link to this heading")

When run in a Jupyter notebook, the schematic will be drawn to the cell output after the with block is exited. If your schematics pop up in an external window, and you are using the Matplotlib backend, set Matplotlib to inline mode before importing schemdraw:

%matplotlib inline

For best results when viewing circuits in the notebook, use a vector figure format, such as svg before importing schemdraw:

%config InlineBackend.figure\_format \= 'svg'

#### Python Scripts and GUI/Web apps[¶](#python-scripts-and-gui-web-apps "Link to this heading")

If run as a Python script, the schematic will be opened in a pop-up window after the with block exits. Add the show=False option when creating the Drawing to suppress the window from appearing.

with schemdraw.Drawing(show\=False) as d:
    ...

The raw image data as a bytes array can be obtained by calling .get\_imagedata() with the after the with block exits. This can be useful for integrating schemdraw into an existing GUI or web application.

with schemdraw.Drawing() as drawing:
    ...
image\_bytes \= drawing.get\_imagedata('svg')

#### Headless Servers[¶](#headless-servers "Link to this heading")

When running on a server, sometimes there is no display available. The code may attempt to open the GUI preview window and fail. In these cases, try setting the Matplotlib backend to a non-GUI option. Before importing schemdraw, add these lines to use the Agg backend which does not have a GUI. Then get the drawing using d.get\_imagedata(), or d.save() to get the image.

import matplotlib
matplotlib.use('Agg') \# Set Matplotlib's backend here

Alternatively, use Schemdraw’s SVG backend (see [Backends](index.html#backends)).

### Saving Drawings[¶](#saving-drawings "Link to this heading")

To save the schematic to a file, add the file parameter when setting up the Drawing. The image type is determined from the file extension. Options include svg, eps, png, pdf, and jpg when using the Matplotlib backend, and svg when using the SVG backend. A vector format such as svg is recommended for best image quality.

with schemdraw.Drawing(file\='my\_circuit.svg') as d:
    ...

The Drawing may also be saved using with the [`schemdraw.Drawing.save()`](index.html#schemdraw.Drawing.save "schemdraw.Drawing.save") method.

Usage[¶](#usage "Link to this heading")
---------------------------------------

### Placing Elements[¶](#placing-elements "Link to this heading")

Elements are added to a Drawing using the add method or += shortcut. The Drawing maintains a current position and direction, such that the default placement of the next element will start at the end of the previous element, going in the same direction.

with schemdraw.Drawing() as d:
    d += elm.Capacitor()
    d += elm.Resistor()
    d += elm.Diode()

![_images/placement_1_0.svg](_images/placement_1_0.svg)

If a direction method (up, down, left, right) is added to an element, the element is rotated in that direction, and future elements take the same direction:

with schemdraw.Drawing() as d:
    d += elm.Capacitor()
    d += elm.Resistor().up()
    d += elm.Diode()

![_images/placement_2_0.svg](_images/placement_2_0.svg)

The theta method can be used to specify any rotation angle in degrees.

d += elm.Resistor().theta(20).label('R1')
d += elm.Resistor().label('R2')  \# Takes position and direction from R1

![_images/placement_5_0.svg](_images/placement_5_0.svg)

#### Anchors[¶](#anchors "Link to this heading")

All elements have a set of predefined “anchor” positions within the element. For example, a bipolar transistor has base, emitter, and collector anchors. All two-terminal elements have anchors named start, center, and end. The docstring for each element lists the available anchors. Once an element is added to the drawing, all its anchor positions will be added as attributes to the element object, so the base position of transistor assigned to variable Q may be accessed via Q.base.

Rather than working in absolute (x, y) coordinates, anchors can be used to set the position of new elements. Using the at method, one element can be placed starting on the anchor of another element.

For example, to draw an opamp and place a resistor on the output, store the Opamp instance to a variable. Then call the at method of the new element passing the Opamp.out anchor. After the resistor is drawn, the current drawing position is moved to the endpoint of the resistor.

opamp \= d.add(elm.Opamp())
d.add(elm.Resistor().right().at(opamp.out))

![_images/placement_8_0.svg](_images/placement_8_0.svg)

Python’s walrus operator provides a convenient shorthand notation for adding an element using += and storing it at the same time. The above code can be written equivalently as:

d += (opamp := elm.Opamp())
d += elm.Resistor().right().at(opamp.out)

The second purpose for anchors is aligning new elements with respect to existing elements.

Suppose a resistor has just been placed, and now an Opamp should be connected to the resistor. The anchor method tells the Drawing which input on the Opamp should align with resistor. Here, an Opamp is placed at the end of a resistor, connected to the opamp’s in1 anchor (the inverting input).

d += elm.Resistor().label('R1')
d += elm.Opamp().anchor('in1')

![_images/placement_11_0.svg](_images/placement_11_0.svg)

Compared to anchoring the opamp at in2 (the noninverting input):

d += elm.Resistor().label('R2')
d += elm.Opamp().anchor('in2')

![_images/placement_14_0.svg](_images/placement_14_0.svg)

#### Dimensions[¶](#dimensions "Link to this heading")

The inner zig-zag portion of a resistor has length of 1 unit, while the default lead extensions are 1 unit on each side, making the default total resistor length 3 units. Placement methods such as at and to accept a tuple of (x, y) position in these units.

![_images/placement_15_0.svg](_images/placement_15_0.svg)

This default 2-terminal length can be changed using the unit parameter to the [`schemdraw.Drawing.config()`](index.html#schemdraw.Drawing.config "schemdraw.Drawing.config") method:

with schemdraw.Drawing() as d:
    d.config(unit\=2)
    ...

![_images/placement_16_0.svg](_images/placement_16_0.svg)

#### Two-Terminal Elements[¶](#two-terminal-elements "Link to this heading")

In Schemdraw, a “Two-Terminal Element” is any element that can grow to fill a given length (this includes elements such as the Potentiometer, even though it electrically has three terminals). All two-terminal elements subclass [`schemdraw.elements.Element2Term`](index.html#schemdraw.elements.Element2Term "schemdraw.elements.Element2Term"). They have some additional methods for setting placement and length.

The length method sets an exact length for a two-terminal element. Alternatively, the up, down, left, and right methods on two-terminal elements take a length parameter.

with schemdraw.Drawing() as d:
    d += elm.Dot()
    d += elm.Resistor()
    d += elm.Dot()
    d += elm.Diode().length(6)    d += elm.Dot()

![_images/placement_17_0.svg](_images/placement_17_0.svg)

The to method will set an exact endpoint for a 2-terminal element. The starting point is still the ending location of the previous element. Notice the Diode is stretched longer than the standard element length in order to fill the diagonal distance.

with schemdraw.Drawing() as d:
    R \= d.add(elm.Resistor())
    C \= d.add(elm.Capacitor().up())
    Q \= d.add(elm.Diode().to(R.start))

![_images/placement_18_0.svg](_images/placement_18_0.svg)

The tox and toy methods are useful for placing 2-terminal elements to “close the loop”, without requiring an exact length. They extend the element horizontally or vertically to the x- or y- coordinate of the anchor given as the argument. These methods automatically change the drawing direction. Here, the Line element does not need to specify an exact length to fill the space and connect back with the Source.

d += (C := elm.Capacitor())
d += elm.Diode()
d += elm.Line().down()

\# Now we want to close the loop, but can use \`tox\`
\# to avoid having to know exactly how far to go.
\# The Line will extend horizontally to the same x-position
\# as the Capacitor's \`start\` anchor.
d += elm.Line().tox(C.start)
\# Now close the loop by relying on the fact that all
\# two-terminal elements (including Source and Line)
\# are the same length by default
d += elm.Source().up()

![_images/placement_21_0.svg](_images/placement_21_0.svg)

Finally, exact endpoints can also be specified using the endpoints method.

d += (R := elm.Resistor())
d += (Q := elm.Diode().down(6))
d += elm.Line().tox(R.start)
d += elm.Capacitor().toy(R.start)
d += elm.SourceV().endpoints(Q.end, R.start)

![_images/placement_24_0.svg](_images/placement_24_0.svg)

#### Orientation[¶](#orientation "Link to this heading")

The flip and reverse methods are useful for changing orientation of directional elements such as Diodes, but they do not affect the drawing direction.

d += elm.Zener().label('Normal')
d += elm.Zener().flip().label('Flip')
d += elm.Zener().reverse().label('Reverse')

![_images/placement_27_0.svg](_images/placement_27_0.svg)

#### Drawing State[¶](#drawing-state "Link to this heading")

The [`schemdraw.Drawing`](index.html#schemdraw.Drawing "schemdraw.Drawing") maintains a drawing state that includes the current x, y position, stored in the Drawing.here attribute as a (x, y) tuple, and drawing direction stored in the Drawing.theta attribute. A LIFO stack of drawing states can be used, via the [`schemdraw.Drawing.push()`](index.html#schemdraw.Drawing.push "schemdraw.Drawing.push") and [`schemdraw.Drawing.pop()`](index.html#schemdraw.Drawing.pop "schemdraw.Drawing.pop") method, for situations when it’s useful to save the drawing state and come back to it later.

d += elm.Inductor()
d += elm.Dot()
print('d.here:', d.here)
d.push()  \# Save this drawing position/direction for later
d += elm.Capacitor().down()  \# Go off in another direction temporarily
d += elm.Ground(lead\=False)
print('d.here:', d.here)

d.pop()   \# Return to the pushed position/direction
print('d.here:', d.here)
d += elm.Diode()
d.draw()

d.here: Point(3.0,0.0)
d.here: Point(2.9999999999999996,-3.0)
d.here: Point(3.0,0.0)

![_images/placement_29_1.svg](_images/placement_29_1.svg)

Changing the drawing position can be accomplished by calling [`schemdraw.Drawing.move()`](index.html#schemdraw.Drawing.move "schemdraw.Drawing.move") or [`schemdraw.Drawing.move_from()`](index.html#schemdraw.Drawing.move_from "schemdraw.Drawing.move_from").

##### Drop and Hold Methods[¶](#drop-and-hold-methods "Link to this heading")

To place an element without moving the drawing position, use the [`schemdraw.elements.Element.hold()`](index.html#schemdraw.elements.Element.hold "schemdraw.elements.Element.hold") method. The element will be placed without changing the drawing state.

d += elm.Diode()  \# Normal placement: drawing position moves to end of element
d += elm.Dot().color('red')

d.here \= (0, \-1)
d += elm.Diode().hold()  \# Hold method prevents position from changing
d += elm.Dot().color('blue')

![_images/placement_32_0.svg](_images/placement_32_0.svg)

Three-terminal elements do not necessarily leave the drawing position where desired, so after drawing an element, the current drawing position can be set using the [`schemdraw.elements.Element.drop()`](index.html#schemdraw.elements.Element.drop "schemdraw.elements.Element.drop") method to specify an anchor at which to place the cursor. This reduces the need to assign every element to a variable name.

d += elm.BjtNpn()
d += elm.Resistor().label('R1')
d.here \= (5, 0)

d += elm.BjtNpn().drop('emitter')
d += elm.Resistor().label('R2')

![_images/placement_35_0.svg](_images/placement_35_0.svg)

#### Connecting Elements[¶](#connecting-elements "Link to this heading")

Typically, the [`schemdraw.elements.lines.Line`](index.html#schemdraw.elements.lines.Line "schemdraw.elements.lines.Line") element is used to connect elements together. More complex line routing requires multiple Line elements. The [`schemdraw.elements.lines.Wire`](index.html#schemdraw.elements.lines.Wire "schemdraw.elements.lines.Wire") element is used as a shortcut for placing multiple connecting lines at once. The Wire element connects the start and end points based on its shape parameter. The k parameter is used to set the distance before the wire first changes direction.

Wire Shape Parameters[¶](#id1 "Link to this table")  

Shape Parameter

Description

\-

Direct Line

\-|

Horizontal then vertical

|-

Vertical then horizontal

n

Vertical-horizontal-vertical (like an n or u)

c

Horizontal-vertical-horizontal (like a c or ↄ)

z

Horizontal-diagonal-horizontal

N

Vertical-diagonal-vertical

d += elm.Wire('-', arrow\='->').at(A.center).to(B.center).color('deeppink').label('"-"')
d += elm.Wire('|-', arrow\='->').at(A.center).to(B.center).color('mediumblue').label('"|-"')
d += elm.Wire('-|', arrow\='->').at(A.center).to(B.center).color('darkseagreen').label('"-|"')
d += elm.Wire('c', k\=-1, arrow\='->').at(C.center).to(D.center).color('darkorange').label('"c"', halign\='left')
d += elm.Wire('n', arrow\='->').at(C.center).to(D.center).color('orchid').label('"n"')
d += elm.Wire('N', arrow\='->').at(E.center).to(F.center).color('darkred').label('"N"', 'start', ofst\=(\-.1, \-.75))
d += elm.Wire('z', k\=.5, arrow\='->').at(E.center).to(F.center).color('teal').label('"z"', halign\='left', ofst\=(0, .5))

![_images/placement_38_0.svg](_images/placement_38_0.svg)

Both Line and Wire elements take an arrow parameter, a string specification of arrowhead types at the start and end of the wire. The arrow string may contain “<”, “>”, for arrowheads, “|” for an endcap, and “o” for a dot. Some examples are shown below:

d += elm.Line(arrow\='->').label('"->"', 'right')
d += elm.Line(arrow\='<-').at((0, \-.75)).label('"<-"', 'right')
d += elm.Line(arrow\='<->').at((0, \-1.5)).label('"<->"', 'right')
d += elm.Line(arrow\='|->').at((0, \-2.25)).label('"|->"', 'right')
d += elm.Line(arrow\='|-o').at((0, \-3.0)).label('"|-o"', 'right')

![_images/placement_41_0.svg](_images/placement_41_0.svg)

Because dots are used to show connected wires, all two-terminal elements have dot and idot methods for quickly adding a dot at the end or beginning of the element, respectively.

elm.Resistor().dot()

![_images/placement_42_0.svg](_images/placement_42_0.svg)

#### Keyword Arguments[¶](#keyword-arguments "Link to this heading")

All [`schemdraw.elements.Element`](index.html#schemdraw.elements.Element "schemdraw.elements.Element") types take keyword arguments that can also be used to set element properties, partly for historical reasons but also for easy element setup via dictionary unpacking. The keyword arguments are equivalent to calling the Element setup methods. The keyword arguments are not validated or type checked, so the chained method interface described above is recommended for configuring elements.

Keyword Argument

Method Equivalent

d=’up’

.up()

d=’down’

.down()

d=’left’

.left()

d=’right’

.right()

theta=X

.theta(X)

at=X or xy=X

.at(X)

flip=True

.flip()

reverse=True

.reverse()

anchor=X

.anchor(X)

zoom=X

.scale(X)

color=X

.color(X)

fill=X

.fill(X)

ls=X

.linestyle(X)

lw=X

.linewidth(X)

zorder=X

.zorder(X)

move\_cur=False

.hold()

label=X

.label(X)

botlabel=X

.label(X, loc=’bottom’)

lftlabel=X

.label(X, loc=’left’)

rgtlabel=X

.label(X, loc=’right’)

toplabel=X

.label(X, loc=’top’)

lblloc=X

.label(…, loc=X)

### Labels[¶](#labels "Link to this heading")

Labels are added to elements using the [`schemdraw.elements.Element.label()`](index.html#schemdraw.elements.Element.label "schemdraw.elements.Element.label") method. Some unicode utf-8 characters are allowed, such as `'1μF'` and `'1MΩ'` if the character is included in your font set. Alternatively, full LaTeX math expressions can be rendered when enclosed in $..$ For a description of supported math expressions, in the Matplotlib backend see [Matplotlib Mathtext](https://matplotlib.org/stable/tutorials/text/mathtext.html), and the SVG backend refer to the [Ziamath](https://ziamath.readthedocs.io) package. Subscripts and superscripts are also added using LaTeX math mode, enclosed in $..$:

d += elm.Resistor().label('1MΩ')
d += elm.Capacitor().label('1μF')
d += elm.Capacitor().label(r'$v = \\frac{1}{C} \\int i dt$')
d += elm.Resistor().at((0, \-2)).label('$R\_0$')
d += elm.Capacitor().label('$x^2$')

![_images/labels_3_0.svg](_images/labels_3_0.svg)

#### Location[¶](#location "Link to this heading")

The label location is specified with the loc parameter to the label method. It can be left, right, top, bottom, or the name of a defined anchor within the element. These directions do not depend on rotation. A label with loc=’left’ is always on the leftmost terminal of the element.

d += (elm.Resistor()
        .label('Label')  \# 'top' is default
        .label('Bottom', loc\='bottom')
        .label('Right', loc\='right')
        .label('Left', loc\='left'))

![_images/labels_6_0.svg](_images/labels_6_0.svg)

Labels may also be placed near an element anchor by giving the anchor name as the loc parameter.

d += (elm.BjtNpn()
        .label('b', loc\='base')
        .label('c', loc\='collector')
        .label('e', loc\='emitter'))

![_images/labels_9_0.svg](_images/labels_9_0.svg)

The [`schemdraw.elements.Element.label()`](index.html#schemdraw.elements.Element.label "schemdraw.elements.Element.label") method also takes parameters that control the label’s rotation, offset, font, alignment, and color. Label text stays horizontal by default, but may be rotated to the same angle as the element using rotate=True, or any angle X in degrees with rotate=X. Offsets apply vertically if a float value is given, or in both x and y if a tuple is given.

d += elm.Resistor().label('no offset')
d += elm.Resistor().label('offset', ofst\=1)
d += elm.Resistor().label('offset (x, y)', ofst\=(\-.6, .2))
d += elm.Resistor().theta(\-45).label('no rotate')
d += elm.Resistor().theta(\-45).label('rotate', rotate\=True)
d += elm.Resistor().theta(45).label('90°', rotate\=90)

![_images/labels_12_0.svg](_images/labels_12_0.svg)

Labels may also be added anywhere using the [`schemdraw.elements.lines.Label`](index.html#schemdraw.elements.lines.Label "schemdraw.elements.lines.Label") element. The element itself draws nothing, but labels can be added to it:

elm.Label().label('Hello')

#### Voltage Labels[¶](#voltage-labels "Link to this heading")

A label may also be a list/tuple of strings, which will be evenly-spaced along the length of the element. This allows for labeling positive and negative along with a component name, for example:

d += elm.Resistor().label(('–','$V\_1$','+'))  \# Note: using endash U+2013 character

![_images/labels_15_0.svg](_images/labels_15_0.svg)

Use the Gap element to label voltage across a terminal:

d += elm.Line().dot(open\=True)
d += elm.Gap().label(('–','$V\_o$','+'))
d += elm.Line().idot(open\=True)

![_images/labels_18_0.svg](_images/labels_18_0.svg)

#### Current Arrow Labels[¶](#current-arrow-labels "Link to this heading")

##### Current Arrow[¶](#current-arrow "Link to this heading")

To label the current through an element, the [`schemdraw.elements.lines.CurrentLabel`](index.html#schemdraw.elements.lines.CurrentLabel "schemdraw.elements.lines.CurrentLabel") element can be added. The at method of this element can take an Element instance to label, and the arrow will be placed over the center of that Element.

d += (R1 := elm.Resistor())
d += elm.CurrentLabel().at(R1).label('10 mA')

![_images/labels_21_0.svg](_images/labels_21_0.svg)

For transistors, the label will follow sensible bias currents by default.

d += (Q1 := elm.AnalogNFet())
d += elm.CurrentLabel().at(Q1).label('10 µA')

d += (Q2 := elm.AnalogNFet()).at(\[4,0\]).flip().reverse()
d += elm.CurrentLabel().at(Q2).label('10 µA')

![_images/labels_24_0.svg](_images/labels_24_0.svg)

##### Inline Current Arrow[¶](#inline-current-arrow "Link to this heading")

Alternatively, current labels can be drawn inline as arrowheads on the leads of 2-terminal elements using [`schemdraw.elements.lines.CurrentLabelInline`](index.html#schemdraw.elements.lines.CurrentLabelInline "schemdraw.elements.lines.CurrentLabelInline"). Parameters direction and start control whether the arrow is shown pointing into or out of the element, and which end to place the arrowhead on.

d += (R1 := elm.Resistor())
d += elm.CurrentLabelInline(direction\='in').at(R1).label('10 mA')

![_images/labels_27_0.svg](_images/labels_27_0.svg)

##### Loop Current[¶](#loop-current "Link to this heading")

Loop currents can be added using [`schemdraw.elements.lines.LoopCurrent`](index.html#schemdraw.elements.lines.LoopCurrent "schemdraw.elements.lines.LoopCurrent"), given a list of 4 existing elements surrounding the loop.

d += (R1 := elm.Resistor())
d += (C1 := elm.Capacitor().down())
d += (D1 := elm.Diode().fill(True).left())
d += (L1 := elm.Inductor().up())
d += elm.LoopCurrent(\[R1, C1, D1, L1\], direction\='cw').label('$I\_1$')

![_images/labels_30_0.svg](_images/labels_30_0.svg)

Alternatively, loop current arrows can be added anywhere with any size using [`schemdraw.elements.lines.LoopArrow`](index.html#schemdraw.elements.lines.LoopArrow "schemdraw.elements.lines.LoopArrow").

d += (a:=elm.Line().dot())
d += elm.LoopArrow(width\=.75, height\=.75).at(a.end)

![_images/labels_33_0.svg](_images/labels_33_0.svg)

##### Impedance Arrow Label[¶](#impedance-arrow-label "Link to this heading")

A right-angle arrow label, often used to indicate impedance looking into a node, is added using [`schemdraw.elements.lines.ZLabel`](index.html#schemdraw.elements.lines.ZLabel "schemdraw.elements.lines.ZLabel").

d += (R:=elm.RBox().right())
d += elm.ZLabel().at(R).label('$Z\_{in}$')

![_images/labels_36_0.svg](_images/labels_36_0.svg)

#### Annotations[¶](#annotations "Link to this heading")

To make text and arrow annotations to a schematic, the [`schemdraw.elements.lines.Annotate`](index.html#schemdraw.elements.lines.Annotate "schemdraw.elements.lines.Annotate") element draws a curvy arrow with label placed at it’s end. It is based on the [`schemdraw.elements.lines.Arc3`](index.html#schemdraw.elements.lines.Arc3 "schemdraw.elements.lines.Arc3") element.

The [`schemdraw.elements.lines.Encircle`](index.html#schemdraw.elements.lines.Encircle "schemdraw.elements.lines.Encircle") and [`schemdraw.elements.lines.EncircleBox`](index.html#schemdraw.elements.lines.EncircleBox "schemdraw.elements.lines.EncircleBox") elements draw an ellipse, or rounded rectangle, surrounding a list of elements.

d += (parallel := elm.Encircle(\[R1, R2\], padx\=.8).linestyle('--').linewidth(1).color('red'))
d += (series := elm.Encircle(\[R3, R4\], padx\=.8).linestyle('--').linewidth(1).color('blue'))

d += elm.Annotate().at(parallel.NNE).delta(dx\=1, dy\=1).label('Parallel').color('red')
d += elm.Annotate(th1\=0).at(series.ENE).delta(dx\=1.5, dy\=1).label('Series').color('blue')

![_images/labels_39_0.svg](_images/labels_39_0.svg)

### Styling[¶](#styling "Link to this heading")

Style options, such as color, line thickness, and fonts, may be set at the global level (all Schemdraw Drawings), at the Drawing level, or on individual Elements.

#### Individual Elements[¶](#individual-elements "Link to this heading")

Element styling methods include color, fill, linewidth, and linestyle. If a style method is not called when creating an Element, its value is obtained from from the drawing or global defaults.

Color and fill parameters accept any named [SVG color](https://upload.wikimedia.org/wikipedia/commons/2/2b/SVG_Recognized_color_keyword_names.svg) or a hex color string such as ‘#6A5ACD’. Linestyle parameters may be ‘-’, ‘–’, ‘:’, or ‘-.’.

\# All elements are blue with lightgray fill unless specified otherwise
d \= schemdraw.Drawing(color\='blue', fill\='lightgray')

d += elm.Diode()
d += elm.Diode().fill('red')        \# Fill overrides drawing color here
d += elm.Resistor().fill('purple')  \# Fill has no effect on non-closed elements
d += elm.RBox().linestyle('--').color('orange')
d += elm.Resistor().linewidth(5)

![_images/styles_2_01.svg](_images/styles_2_01.svg)

The label method also accepts color, font, and fontsize parameters, allowing labels with different style as their elements.

#### Drawing style[¶](#drawing-style "Link to this heading")

Styles may be applied to an entire drawing using the [`schemdraw.Drawing.config()`](index.html#schemdraw.Drawing.config "schemdraw.Drawing.config") method. These parameters include color, linewidth, font, fontsize, linestyle, fill, and background color. Additionally, the config method allows specification of the default 2-Terminal element length.

#### Global style[¶](#global-style "Link to this heading")

Styles may be applied to every new drawing created by Schemdraw (during the Python session) using [`schemdraw.config()`](index.html#schemdraw.config "schemdraw.config"), using the same arguments as the Drawing config method.

schemdraw.config(lw\=1, font\='serif')
with schemdraw.Drawing() as d:
    d += elm.Resistor().label('100KΩ')
    d += elm.Capacitor().down().label('0.1μF', loc\='bottom')
    d += elm.Line().left()
    d += elm.Ground()
    d += elm.SourceV().up().label('10V')

![_images/styles_3_0.svg](_images/styles_3_0.svg)

#### Global Element Configuration[¶](#global-element-configuration "Link to this heading")

The [`schemdraw.elements.Element.style()`](index.html#schemdraw.elements.Element.style "schemdraw.elements.Element.style") can be used to configure styles on individual element classes that apply to all Drawings. It may be used, for example, to fill all Diode elements by default, without requiring the fill() method on every Diode instance.

Its argument is a dictionary of {name: Element} class pairs. Combined with [functools.partial](https://docs.python.org/3/library/functools.html#functools.partial) from the standard library, parameters to elements can be set globally. For example, the following code fills all Diode elements:

from functools import partial

elm.style({'Diode': partial(elm.Diode, fill\=True)})
with schemdraw.Drawing() as d:
    d += elm.Diode()
    d += elm.Diode()

![_images/styles_5_0.svg](_images/styles_5_0.svg)

Be careful, though, because the style method can overwrite existing elements in the namespace.

#### U.S. versus European Style[¶](#u-s-versus-european-style "Link to this heading")

The main use of [`schemdraw.elements.Element.style()`](index.html#schemdraw.elements.Element.style "schemdraw.elements.Element.style") is to reconfigure elements in IEEE/U.S. style or IEC/European style. The schemdraw.elements.STYLE\_IEC and schemdraw.elements.STYLE\_IEEE are dictionaries for use in the style method to change configuration of various elements that use different standard symbols (resistor, variable resistor, photo resistor, etc.)

To configure IEC/European style, use the style method with the elm.STYLE\_IEC dictionary.

elm.style(elm.STYLE\_IEC)
d += elm.Resistor()

![_images/styles_8_0.svg](_images/styles_8_0.svg)

elm.style(elm.STYLE\_IEEE)
d += elm.Resistor()

![_images/styles_11_0.svg](_images/styles_11_0.svg)

To see all the elements that change between IEEE and IEC, see [Styled Elements](index.html#styledelements).

#### Fonts[¶](#fonts "Link to this heading")

The font for label text may be set using the font parameter, either in the [`schemdraw.elements.Element.label()`](index.html#schemdraw.elements.Element.label "schemdraw.elements.Element.label") method for a single label, or in [`schemdraw.Drawing.config()`](index.html#schemdraw.Drawing.config "schemdraw.Drawing.config") to set the font for the entire drawing. The font parameter may be a string containing the name of a font installed in the system fonts path, a path to a TTF font file, or the name of a font family such as “serif” or “sans”. These font options apply whether working in the Matplotlib or SVG backends.

with schemdraw.Drawing() as d:
    \# Default font
    d += elm.RBox().label('R1\\n500K')

    \# Named font in system fonts path
    d += elm.RBox().label('R1\\n500K', font\='Comic Sans MS')

    \# Path to a TTF file
    d += elm.RBox().label('R1\\n500K', font\='Peralta-Regular.ttf')

    \# Font family
    d += elm.RBox().label('R1\\n500K', font\='serif')

![Font examples](_images/fonts.svg)

For typesetting math expressions, the mathfont parameter is used. In the Matplotlib backend, a limited [selection of math fonts](https://matplotlib.org/stable/tutorials/text/mathtext.html#fonts) are available. With the SVG backend in the path text mode, the mathfont parameter may be the path to any TTF file that contains a MATH table (requires [Ziamath](https://ziamath.readthedocs.io)).

with schemdraw.Drawing(canvas\='svg') as d:
    \# Default math font
    d += elm.RBox().label(r'$\\sqrt{a^2+b^2}$').at((0, \-2))

    \# Path to a TTF file with MATH font table (SVG backend only)
    d += elm.RBox().label(r'$\\sqrt{a^2+b^2}$', mathfont\='Asana-Math.ttf')

![Math font examples](_images/mathfonts.svg)

#### Themes[¶](#themes "Link to this heading")

Schemdraw also supports themeing, to enable dark mode, for example. The defined themes match those in the [Jupyter Themes](https://github.com/dunovank/jupyter-themes) package:

> *   default (black on white)
>     
> *   dark (white on black)
>     
> *   solarizedd
>     
> *   solarizedl
>     
> *   onedork
>     
> *   oceans16
>     
> *   monokai
>     
> *   gruvboxl
>     
> *   gruvboxd
>     
> *   grade3
>     
> *   chesterish
>     

They are enabled using [`schemdraw.theme()`](index.html#schemdraw.theme "schemdraw.theme"):

schemdraw.theme('monokai')
with schemdraw.Drawing() as d:
    d += elm.Resistor().label('100KΩ')
    d += elm.Capacitor().down().label('0.1μF', loc\='bottom')
    d += elm.Line().left()
    d += elm.Ground()
    d += elm.SourceV().up().label('10V')

![_images/styles_12_0.svg](_images/styles_12_0.svg)

### Backends[¶](#backends "Link to this heading")

The backend is the “canvas” on which a schematic is drawn. Schemdraw supports two backends: Matplotlib, and SVG.

#### Matplotlib Backend[¶](#matplotlib-backend "Link to this heading")

By default, all schematics are drawn on a Matplotlib axis. A new Matplotlib Figure and Axis will be created, with no frame or borders. A schematic may be added to an existing Axis by using the [`schemdraw.Drawing.draw()`](index.html#schemdraw.Drawing.draw "schemdraw.Drawing.draw") method and setting the canvas parameter to an existing Axis instance.

The Matplotlib backend renders text labels as primative lines and arcs rather than text elements by default. This has the downside that SVG editors, such as Inkscape, cannot perform textual searches on the SVGs. The upside is that there is no dependence on installed fonts on the hosts that open the SVGs.

To configure Matplotlib to render labels as SVG text elements:

import matplotlib
matplotlib.rcParams\['svg.fonttype'\] \= 'none'

#### SVG Backend[¶](#svg-backend "Link to this heading")

Schematics can also be drawn on directly to an SVG image backend. The SVG backend can be enabled for all drawings by calling:

schemdraw.use('svg')

The backend can be changed at any time. Alternatively, the backend can be set individually on each Drawing using the canvas parameter:

with schemdraw.Drawing(canvas\='svg') as d:
    ...

Use additional Python libraries, such as [pycairo](https://cairosvg.org/), to convert the SVG output into other image formats.

##### Math Text[¶](#math-text "Link to this heading")

The SVG backend has basic math text support, including greek symbols, subscripts, and superscripts. However, if [ziamath](https://ziamath.readthedocs.io) and [latex2mathml](https://pypi.org/project/latex2mathml/) packages are installed, they will be used for full Latex math support.

The SVG backend can produce searchable-text SVGs by setting:

schemdraw.svgconfig.text \= 'text'

However, text mode does not support full Latex compatibility. To switch back to rendering text as SVG paths:

schemdraw.svgconfig.text \= 'path'

Some SVG renderers are not fully compatible with SVG2.0. For better compatibility with SVG1.x, use

schemdraw.svgconfig.svg2 \= False

The decimal precision of SVG elements can be set using

schemdraw.svgconfig.precision \= 2

#### Backend Comparison[¶](#backend-comparison "Link to this heading")

Reasons to choose the SVG backend include:

> *   No Matplotlib/Numpy dependency required (huge file size savings if bundling an executable).
>     
> *   Speed. The SVG backend draws 4-10x faster than Matplotlib, depending on the circuit complexity.
>     

Reasons to use Matplotlib backend:

> *   To customize the schematic after drawing it by using other Matplotlib functionality.
>     
> *   To render directly in other, non-SVG, image formats, with no additional code.
>     

Circuit Elements[¶](#circuit-elements "Link to this heading")
-------------------------------------------------------------

### Basic Elements[¶](#basic-elements "Link to this heading")

See [Electrical Elements](index.html#elecelements) for complete class definitions for these elements.

#### Two-terminal[¶](#two-terminal "Link to this heading")

Two-terminal devices subclass [`schemdraw.elements.Element2Term`](index.html#schemdraw.elements.Element2Term "schemdraw.elements.Element2Term"), and have leads that will be extended to make the element the desired length depending on the arguments. All two-terminal elements define start, end, and center anchors for placing, and a few define other anchors as shown in blue in the tables below. Some elements have optional parameters, shown in parenthesis in the table below.

##### Styled Elements[¶](#styled-elements "Link to this heading")

These elements change based on IEEE/U.S. vs IEC/European style configured by [`schemdraw.elements.style()`](index.html#schemdraw.elements.style "schemdraw.elements.style"). Selectable elements, such as Resistor, point to either ResistorIEEE or ResistorIEC, for example.

###### IEEE Style[¶](#ieee-style "Link to this heading")

IEEE style, common in the U.S., is the default, or it can be configured using

elm.style(elm.STYLE\_IEEE)

![_images/electrical_1_0.svg](_images/electrical_1_0.svg)

###### IEC/European Style[¶](#iec-european-style "Link to this heading")

IEC style can be enabled using

elm.style(elm.STYLE\_IEC)

![_images/electrical_2_0.svg](_images/electrical_2_0.svg)

##### Resistors[¶](#resistors "Link to this heading")

Both styles of resistors are always available using these classes.

![_images/electrical_3_0.svg](_images/electrical_3_0.svg)

##### Capacitors and Inductors[¶](#capacitors-and-inductors "Link to this heading")

![_images/electrical_4_0.svg](_images/electrical_4_0.svg)

##### Diodes[¶](#diodes "Link to this heading")

![_images/electrical_5_0.svg](_images/electrical_5_0.svg)

##### Pathological[¶](#pathological "Link to this heading")

![_images/electrical_6_0.svg](_images/electrical_6_0.svg)

##### Miscellaneous[¶](#miscellaneous "Link to this heading")

![_images/electrical_7_0.svg](_images/electrical_7_0.svg)

##### Sources and Meters[¶](#sources-and-meters "Link to this heading")

![_images/electrical_8_0.svg](_images/electrical_8_0.svg)

##### Switches[¶](#switches "Link to this heading")

![_images/electrical_9_0.svg](_images/electrical_9_0.svg)

##### Lines and Arrows[¶](#lines-and-arrows "Link to this heading")

![_images/electrical_10_0.svg](_images/electrical_10_0.svg)

#### Single-Terminal[¶](#single-terminal "Link to this heading")

Single terminal elements are drawn about a single point, and do not move the current drawing position.

##### Power and Ground[¶](#power-and-ground "Link to this heading")

![_images/electrical_11_0.svg](_images/electrical_11_0.svg)

##### Antennas[¶](#antennas "Link to this heading")

![_images/electrical_12_0.svg](_images/electrical_12_0.svg)

##### Connection Dots[¶](#connection-dots "Link to this heading")

![_images/electrical_13_0.svg](_images/electrical_13_0.svg)

#### Switches[¶](#id1 "Link to this heading")

The standard toggle switch is listed with other two-terminal elements above. Other switch configurations are shown here.

##### Single-pole double-throw[¶](#single-pole-double-throw "Link to this heading")

Two options for SPDT switches can be also be drawn with arrows by adding action=’open’ or action=’close’ parameters.

![_images/electrical_14_0.svg](_images/electrical_14_0.svg)

##### Double-pole[¶](#double-pole "Link to this heading")

DPST and DPDT switches have a link parameter for disabling the dotted line lnking the poles.

![_images/electrical_15_0.svg](_images/electrical_15_0.svg)

##### Rotary Switch[¶](#rotary-switch "Link to this heading")

The rotary switch [`schemdraw.elements.switches.SwitchRotary`](index.html#schemdraw.elements.switches.SwitchRotary "schemdraw.elements.switches.SwitchRotary") takes several parameters, with n being the number of contacts and other parameters defining the contact placement.

![_images/electrical_16_0.svg](_images/electrical_16_0.svg)

##### DIP Switch[¶](#dip-switch "Link to this heading")

A set of switches in a dual-inline package, where can show each switch flipped up or down. See [`schemdraw.elements.switches.SwitchDIP`](index.html#schemdraw.elements.switches.SwitchDIP "schemdraw.elements.switches.SwitchDIP") for options.

![_images/electrical_17_0.svg](_images/electrical_17_0.svg)

#### Audio Elements[¶](#audio-elements "Link to this heading")

Speakers, Microphones, Jacks

![_images/electrical_18_0.svg](_images/electrical_18_0.svg)

![_images/electrical_19_0.svg](_images/electrical_19_0.svg)

#### Labels[¶](#labels "Link to this heading")

The Label element can be used to add a label anywhere. The Gap is like an “invisible” element, useful for marking the voltage between output terminals.

![_images/electrical_20_0.svg](_images/electrical_20_0.svg)

#### Operational Amplifiers[¶](#operational-amplifiers "Link to this heading")

The [`schemdraw.elements.opamp.Opamp`](index.html#schemdraw.elements.opamp.Opamp "schemdraw.elements.opamp.Opamp") element defines several anchors for various inputs, including voltage supplies and offset nulls. Optional leads can be added using the leads parameter, with anchors exteded to the ends of the leads.

![_images/electrical_21_0.svg](_images/electrical_21_0.svg)

#### Transistors[¶](#transistors "Link to this heading")

##### Bipolar Junction Transistors[¶](#bipolar-junction-transistors "Link to this heading")

![_images/electrical_22_0.svg](_images/electrical_22_0.svg)

##### Field-Effect Transistors[¶](#field-effect-transistors "Link to this heading")

![_images/electrical_23_0.svg](_images/electrical_23_0.svg)

##### “Two-Terminal” Transistors[¶](#two-terminal-transistors "Link to this heading")

Another set of transistor elements subclass [`schemdraw.elements.Element2Term`](index.html#schemdraw.elements.Element2Term "schemdraw.elements.Element2Term") so they have emitter and collector (or source and drain) leads extended to the desired length. These can be easier to place centered between endpoints, for example.

![_images/electrical_24_0.svg](_images/electrical_24_0.svg)

#### Two-ports[¶](#two-ports "Link to this heading")

Twoport elements share the interface defined by [`schemdraw.elements.twoports.ElementTwoport`](index.html#schemdraw.elements.twoports.ElementTwoport "schemdraw.elements.twoports.ElementTwoport"), providing a set of anchors and various styling options. The terminals and box can be enabled or disabled using the terminals and box arguments. In addition, the boxfill, boxlw, and boxls provide the option to style the outline separately from other elements.

![_images/electrical_25_0.svg](_images/electrical_25_0.svg)

##### Generic[¶](#generic "Link to this heading")

![_images/electrical_26_0.svg](_images/electrical_26_0.svg)

##### Transactors (ideal amplifiers)[¶](#transactors-ideal-amplifiers "Link to this heading")

Like the generic twoport, the transactors provide the option to reverse the direction of the output or current using the reverse\_output argument.

![_images/electrical_27_0.svg](_images/electrical_27_0.svg)

##### Pathological[¶](#id2 "Link to this heading")

![_images/electrical_28_0.svg](_images/electrical_28_0.svg)

##### Custom[¶](#custom "Link to this heading")

The [`schemdraw.elements.twoports.ElementTwoport`](index.html#schemdraw.elements.twoports.ElementTwoport "schemdraw.elements.twoports.ElementTwoport") class can be used to define custom twoports by specifying an input\_element and output\_element. The bpadx, bpady, minw, unit, width can be used to tune the horizontal and vertical padding, minimum width of the elements, length of components, and width of the twoport respectively.

d += elm.ElementTwoport(input\_element\=elm.Inductor2(),
                        output\_element\=elm.SwitchReed(),
                        unit\=2.5, width\=2.5).anchor('center')

d += elm.ElementTwoport(input\_element\=elm.Lamp(),
                        output\_element\=elm.Photodiode().reverse().flip(),
                        width\=3).anchor('center').at(\[7,0\])

![_images/electrical_31_0.svg](_images/electrical_31_0.svg)

#### Cables[¶](#cables "Link to this heading")

[`schemdraw.elements.cables.Coax`](index.html#schemdraw.elements.cables.Coax "schemdraw.elements.cables.Coax") and [`schemdraw.elements.cables.Triax`](index.html#schemdraw.elements.cables.Triax "schemdraw.elements.cables.Triax") cables are 2-Terminal elements that can be made with several options and anchors. Coax parameters include length, radius, and leadlen for setting the distance between leads and the shell. Triax parameters include length, radiusinner, radiusouter, leadlen, and shieldofststart for offseting the outer shield from the inner guard.

![_images/electrical_32_0.svg](_images/electrical_32_0.svg)

![_images/electrical_33_0.svg](_images/electrical_33_0.svg)

#### Transformers[¶](#transformers "Link to this heading")

The [`schemdraw.elements.xform.Transformer`](index.html#schemdraw.elements.xform.Transformer "schemdraw.elements.xform.Transformer") element is used to create various transformers. Anchors p1, p2, s1, and s2 are defined for all transformers. Other anchors can be created using the taps method to add tap locations to either side.

![_images/electrical_34_0.svg](_images/electrical_34_0.svg)

Here is a transformers with anchor “B” added using the tap method. Note the tap by itself does not draw anything, but defines a named anchor to connect to.

with schemdraw.Drawing() as d:
    d.config(fontsize\=12)
    x \= d.add(elm.Transformer(t1\=4, t2\=8)
              .tap(name\='B', pos\=3, side\='secondary'))
    d += elm.Line().at(x.s1).length(d.unit/4).label('s1', 'rgt').color('blue')
    d += elm.Line().at(x.s2).length(d.unit/4).label('s2', 'rgt').color('blue')
    d += elm.Line().at(x.p1).length(d.unit/4).left().label('p1', 'lft').color('blue')
    d += elm.Line().at(x.p2).length(d.unit/4).left().label('p2', 'lft').color('blue')
    d += elm.Line().at(x.B).length(d.unit/4).right().label('B', 'rgt').color('blue')

![_images/electrical_35_0.svg](_images/electrical_35_0.svg)

### Integrated Circuits[¶](#integrated-circuits "Link to this heading")

The [`schemdraw.elements.intcircuits.Ic`](index.html#schemdraw.elements.intcircuits.Ic "schemdraw.elements.intcircuits.Ic") class is used to make integrated circuits, multiplexers, and other black box elements. The [`schemdraw.elements.intcircuits.IcPin`](index.html#schemdraw.elements.intcircuits.IcPin "schemdraw.elements.intcircuits.IcPin") class is used to define each input/output pin before adding it to the Ic.

All pins will be given an anchor name of inXY where X is the side (L, R, T, B), and Y is the pin number along that side. Pins also define anchors based on the name parameter. If the anchorname parameter is provided for the pin, this name will be used, so that the pin name can be any string even if it cannot be used as a Python variable name.

Here, a J-K flip flop, as part of an HC7476 integrated circuit, is drawn with input names and pin numbers.

JK \= elm.Ic(pins\=\[elm.IcPin(name\='>', pin\='1', side\='left'),
                  elm.IcPin(name\='K', pin\='16', side\='left'),
                  elm.IcPin(name\='J', pin\='4', side\='left'),
                  elm.IcPin(name\='$\\overline{Q}$', pin\='14', side\='right', anchorname\='QBAR'),
                  elm.IcPin(name\='Q', pin\='15', side\='right')\],
            edgepadW \= .5,  \# Make it a bit wider
            pinspacing\=1).label('HC7476', 'bottom', fontsize\=12)
display(JK)

![_images/intcircuits_1_0.svg](_images/intcircuits_1_0.svg)

Notice the use of $overline{Q}$ to acheive the label on the inverting output. The anchor positions can be accessed using attributes, such as JK.Q for the non-inverting output. However, inverting output is named $overline{Q}, which is not accessible using the typical dot notation. It could be accessed using getattr(JK, ‘$overline{Q}$’), but to avoid this an alternative anchorname of QBAR was defined.

#### Multiplexers[¶](#multiplexers "Link to this heading")

Multiplexers and demultiplexers are drawn with the [`schemdraw.elements.intcircuits.Multiplexer`](index.html#schemdraw.elements.intcircuits.Multiplexer "schemdraw.elements.intcircuits.Multiplexer") class which wraps the Ic class.

elm.Multiplexer(
    pins\=\[elm.IcPin(name\='C', side\='L'),
          elm.IcPin(name\='B', side\='L'),
          elm.IcPin(name\='A', side\='L'),
          elm.IcPin(name\='Q', side\='R'),
          elm.IcPin(name\='T', side\='B', invert\=True)\],
    edgepadH\=-.5)

![_images/intcircuits_2_0.svg](_images/intcircuits_2_0.svg)

See the [Circuit Gallery](index.html#gallery) for more examples.

#### Seven-Segment Display[¶](#seven-segment-display "Link to this heading")

A seven-segment display, in [`schemdraw.elements.intcircuits.SevenSegment`](index.html#schemdraw.elements.intcircuits.SevenSegment "schemdraw.elements.intcircuits.SevenSegment"), provides a single digit with several options including decimal point and common anode or common cathode mode. The [`schemdraw.elements.intcircuits.sevensegdigit()`](index.html#schemdraw.elements.intcircuits.sevensegdigit "schemdraw.elements.intcircuits.sevensegdigit") method generates a list of Segment objects that can be used to add a digit to another element, for example to make a multi-digit display.

![_images/intcircuits_3_0.svg](_images/intcircuits_3_0.svg)

#### DIP Integrated Circuits[¶](#dip-integrated-circuits "Link to this heading")

Integrated circuits can be drawn in dual-inline package style with [`schemdraw.elements.intcircuits.IcDIP`](index.html#schemdraw.elements.intcircuits.IcDIP "schemdraw.elements.intcircuits.IcDIP"). Anchors allow connecting elements externally to show the IC in a circuit, or interanally to show the internal configuration of the IC (see [741 Opamp, DIP Layout](index.html#dip741).)

![_images/intcircuits_4_0.svg](_images/intcircuits_4_0.svg)

#### Predefined ICs[¶](#predefined-ics "Link to this heading")

A few common integrated circuits are predefined as shown below.

![_images/intcircuits_5_0.svg](_images/intcircuits_5_0.svg)

![_images/intcircuits_6_0.svg](_images/intcircuits_6_0.svg)

![_images/intcircuits_7_0.svg](_images/intcircuits_7_0.svg)

![_images/intcircuits_8_0.svg](_images/intcircuits_8_0.svg)

### Connectors[¶](#connectors "Link to this heading")

All connectors are defined with a default pin spacing of 0.6, matching the default pin spacing of the [`schemdraw.elements.intcircuits.Ic`](index.html#schemdraw.elements.intcircuits.Ic "schemdraw.elements.intcircuits.Ic") class, for easy connection of multiple signals.

#### Headers[¶](#headers "Link to this heading")

A [`schemdraw.elements.connectors.Header`](index.html#schemdraw.elements.connectors.Header "schemdraw.elements.connectors.Header") is a generic Header block with any number of rows and columns. It can have round, square, or screw-head connection points.

![_images/connectors_1_0.svg](_images/connectors_1_0.svg)

Header pins are given anchor names pin1, pin2, etc. Pin number labels and anchor names can be ordered left-to-right (lr), up-to-down (ud), or counterclockwise (ccw) like a traditional IC, depending on the numbering argument. The flip argument can be set True to put pin 1 at the bottom.

![_images/connectors_2_0.svg](_images/connectors_2_0.svg)

A [`schemdraw.elements.connectors.Jumper`](index.html#schemdraw.elements.connectors.Jumper "schemdraw.elements.connectors.Jumper") element is also defined, as a simple rectangle, for easy placing onto a header.

J \= d.add(elm.Header(cols\=2, style\='square'))
d.add(elm.Jumper().at(J.pin3).fill('lightgray'))

![_images/connectors_5_0.svg](_images/connectors_5_0.svg)

#### D-Sub Connectors[¶](#d-sub-connectors "Link to this heading")

Both [`schemdraw.elements.connectors.DB9`](index.html#schemdraw.elements.connectors.DB9 "schemdraw.elements.connectors.DB9") and [`schemdraw.elements.connectors.DB25`](index.html#schemdraw.elements.connectors.DB25 "schemdraw.elements.connectors.DB25") subminiature connectors are defined, with anchors pin1 through pin9 or pin25.

![_images/connectors_6_0.svg](_images/connectors_6_0.svg)

#### Multiple Lines[¶](#multiple-lines "Link to this heading")

The [`schemdraw.elements.connectors.RightLines`](index.html#schemdraw.elements.connectors.RightLines "schemdraw.elements.connectors.RightLines") and [`schemdraw.elements.connectors.OrthoLines`](index.html#schemdraw.elements.connectors.OrthoLines "schemdraw.elements.connectors.OrthoLines") elements are useful for connecting multiple pins of an integrated circuit or header all at once. Both need an at and to location specified, along with the n parameter for setting the number of lines to draw. Use RightLines when the Headers are perpindicular to each other.

D1 \= d.add(elm.Ic(pins\=\[elm.IcPin(name\='A', side\='t', slot\='1/4'),
                        elm.IcPin(name\='B', side\='t', slot\='2/4'),
                        elm.IcPin(name\='C', side\='t', slot\='3/4'),
                        elm.IcPin(name\='D', side\='t', slot\='4/4')\]))
D2 \= d.add(elm.Header(rows\=4).at((5,4)))
d.add(elm.RightLines(n\=4).at(D2.pin1).to(D1.D).label('RightLines'))

![_images/connectors_9_0.svg](_images/connectors_9_0.svg)

OrthoLines draw a z-shaped orthogonal connection. Use OrthoLines when the Headers are parallel but vertically offset. Use the xstart parameter, between 0 and 1, to specify the position where the first OrthoLine turns vertical.

D1 \= d.add(elm.Ic(pins\=\[elm.IcPin(name\='A', side\='r', slot\='1/4'),
                        elm.IcPin(name\='B', side\='r', slot\='2/4'),
                        elm.IcPin(name\='C', side\='r', slot\='3/4'),
                        elm.IcPin(name\='D', side\='r', slot\='4/4')\]))
D2 \= d.add(elm.Header(rows\=4).at((7, \-3)))
d.add(elm.OrthoLines(n\=4).at(D1.D).to(D2.pin1).label('OrthoLines'))

![_images/connectors_12_0.svg](_images/connectors_12_0.svg)

#### Data Busses[¶](#data-busses "Link to this heading")

Sometimes, multiple I/O pins to an integrated circuit are lumped together into a data bus. The connections to a bus can be drawn using the [`schemdraw.elements.connectors.BusConnect`](index.html#schemdraw.elements.connectors.BusConnect "schemdraw.elements.connectors.BusConnect") element, which takes n the number of data lines and an argument. [`schemdraw.elements.connectors.BusLine`](index.html#schemdraw.elements.connectors.BusLine "schemdraw.elements.connectors.BusLine") is simply a wider line used to extend the full bus to its destination.

BusConnect elements define anchors start, end on the endpoints of the wide bus line, and pin1, pin2, etc. for the individual signals.

J \= d.add(elm.Header(rows\=6))
B \= d.add(elm.BusConnect(n\=6).at(J.pin1))
d.add(elm.BusLine().down().at(B.end).length(3))
B2 \= d.add(elm.BusConnect(n\=6).anchor('start').reverse())
d.add(elm.Header(rows\=6).at(B2.pin1).anchor('pin1'))

![_images/connectors_15_0.svg](_images/connectors_15_0.svg)

#### Outlets[¶](#outlets "Link to this heading")

Power outlets and plugs are drawn using OutletX classes, with international styles A through L. Each has anchors hot, neutral, and ground (if applicable). The plug parameter fills the prongs to indicate a plug versus an outlet.

![_images/connectors_16_0.svg](_images/connectors_16_0.svg)

### Compound Elements[¶](#compound-elements "Link to this heading")

Several compound elements defined based on other basic elements.

#### Optocoupler[¶](#optocoupler "Link to this heading")

[`schemdraw.elements.compound.Optocoupler`](index.html#schemdraw.elements.compound.Optocoupler "schemdraw.elements.compound.Optocoupler") can be drawn with or without a base contact.

![_images/compound_1_0.svg](_images/compound_1_0.svg)

#### Relay[¶](#relay "Link to this heading")

[`schemdraw.elements.compound.Relay`](index.html#schemdraw.elements.compound.Relay "schemdraw.elements.compound.Relay") can be drawn with different options for switches and inductor solenoids.

![_images/compound_2_0.svg](_images/compound_2_0.svg)

#### Wheatstone[¶](#wheatstone "Link to this heading")

[`schemdraw.elements.compound.Wheatstone`](index.html#schemdraw.elements.compound.Wheatstone "schemdraw.elements.compound.Wheatstone") can be drawn with or without the output voltage taps. The labels argument specifies a list of labels for each resistor.

![_images/compound_3_0.svg](_images/compound_3_0.svg)

#### Rectifier[¶](#rectifier "Link to this heading")

[`schemdraw.elements.compound.Rectifier`](index.html#schemdraw.elements.compound.Rectifier "schemdraw.elements.compound.Rectifier") draws four diodes at 45 degree angles. The labels argument specifies a list of labels for each diode.

![_images/compound_4_0.svg](_images/compound_4_0.svg)

### Digital Logic[¶](#digital-logic "Link to this heading")

Logic gates can be drawn by importing the [`schemdraw.logic.logic`](index.html#module-schemdraw.logic.logic "schemdraw.logic.logic") module:

from schemdraw import logic

Logic gates are shown below. Gates define anchors for out and in1, in2, etc. Buf, Not, and NotNot, and their Schmitt-trigger counterparts, are two-terminal elements that extend leads.

![_images/logic_1_0.svg](_images/logic_1_0.svg)

Gates with more than 2 inputs can be created using the inputs parameter. With more than 3 inputs, the back of the gate will extend up and down.

logic.Nand(inputs\=3)

![_images/logic_2_0.svg](_images/logic_2_0.svg)

logic.Nor(inputs\=4)

![_images/logic_3_0.svg](_images/logic_3_0.svg)

Finally, any input can be pre-inverted (active low) using the inputnots keyword with a list of input numbers, starting at 1 to match the anchor names, on which to add an invert bubble.

logic.Nand(inputs\=3, inputnots\=\[1\])

![_images/logic_4_0.svg](_images/logic_4_0.svg)

#### Logic Parser[¶](#logic-parser "Link to this heading")

Logic trees can also be created from a string logic expression such as “(a and b) or c” using using [`schemdraw.parsing.logic_parser.logicparse()`](index.html#schemdraw.parsing.logic_parser.logicparse "schemdraw.parsing.logic_parser.logicparse"). The logic parser requires the [pyparsing](https://pyparsing-docs.readthedocs.io/en/latest/) module.

Examples:

from schemdraw.parsing import logicparse
logicparse('not ((w and x) or (y and z))', outlabel\='$\\overline{Q}$')

![_images/logic_5_0.svg](_images/logic_5_0.svg)

logicparse('((a xor b) and (b or c) and (d or e)) or ((w and x) or (y and z))')

![_images/logic_6_0.svg](_images/logic_6_0.svg)

Logicparse understands spelled-out logic functions “and”, “or”, “nand”, “nor”, “xor”, “xnor”, “not”, but also common symbols such as “+”, “&”, “⊕” representing “or”, “and”, and “xor”.

logicparse('¬ (a ∨ b) & (c ⊻ d)')  \# Using symbols

![_images/logic_7_0.svg](_images/logic_7_0.svg)

Use the gateH and gateW parameters to adjust how gates line up:

logicparse('(not a) and b or c', gateH\=.5)

![_images/logic_8_0.svg](_images/logic_8_0.svg)

#### Truth Tables[¶](#truth-tables "Link to this heading")

Simple tables can be drawn using the [`schemdraw.logic.table.Table`](index.html#schemdraw.logic.table.Table "schemdraw.logic.table.Table") class. This class is included in the logic module as its primary purpose was for drawing logical truth tables.

The tables are defined using typical Markdown syntax. The colfmt parameter works like the LaTeX tabular environment parameter for defining lines to draw between table columns: “cc|c” draws three centered columns, with a vertical line before the last column. Each column must be specified with a ‘c’, ‘r’, or ‘l’ for center, right, or left justification Two pipes (||), or a double pipe character (ǁ) draw a double bar between columns. Row lines are added to the table string itself, with either — or \=== in the row.

table \= '''
 A | B | C
\---|---|---
 0 | 0 | 0
 0 | 1 | 0
 1 | 0 | 0
 1 | 1 | 1
'''
logic.Table(table, colfmt\='cc||c')

![_images/logic_9_0.svg](_images/logic_9_0.svg)

#### Karnaugh Maps[¶](#karnaugh-maps "Link to this heading")

Karnaugh Maps, or K-Maps, are useful for simplifying a logical truth table into the smallest number of gates. Schemdraw can draw K-Maps, with 2, 3, or 4 input variables, using the [`schemdraw.logic.kmap.Kmap`](index.html#schemdraw.logic.kmap.Kmap "schemdraw.logic.kmap.Kmap") class.

logic.Kmap(names\='ABCD')

![_images/logic_10_0.svg](_images/logic_10_0.svg)

The names parameter must be a string with 2, 3, or 4 characters, each defining the name of one input variable. The truthtable parameter contains a list of tuples defining the logic values to display in the map. The first len(names) elements are 0’s and 1’s defining the position of the cell, and the last element is the string to display in that cell. The default parameter is a string to show in each cell of the K-Map when that cell is undefined in the truthtable.

For example, this 2x2 K-Map has a ‘1’ in the 01 position, and 0’s elsewhere:

logic.Kmap(names\='AB', truthtable\=\[('01', '1')\])

![_images/logic_11_0.svg](_images/logic_11_0.svg)

K-Maps are typically used by grouping sets of 1’s together. These groupings can be drawn using the groups parameter. The keys of the groups dictionary define which cells to group together, and the values of the dictionary define style parameters for the circle around the group. Each key must be a string of length len(names), with either a 0, 1, or . in each position. As an example, with names=’ABCD’, a group key of “1…” will place a circle around all cells where A=1. Or “.00.” draws a circle around all cells where B and C are both 0. Groups will automatically “wrap” around the edges. Parameters of the style dictionary include color, fill, lw, and ls.

logic.Kmap(names\='ABCD',
           truthtable\=\[('1100', '1'),
                       ('1101', '1'),
                       ('1111', '1'),
                       ('1110', '1'),
                       ('0101', '1'),
                       ('0111', 'X'),
                       ('1101', '1'),
                       ('1111', '1'),
                       ('0000', '1'),
                       ('1000', '1')\],
           groups\={'11..': {'color': 'red', 'fill': '#ff000033'},
                   '.1.1': {'color': 'blue', 'fill': '#0000ff33'},
                   '.000': {'color': 'green', 'fill': '#00ff0033'}})

![_images/logic_12_0.svg](_images/logic_12_0.svg)

### Timing Diagrams[¶](#timing-diagrams "Link to this heading")

Digital timing diagrams may be drawn using the [`schemdraw.logic.timing.TimingDiagram`](index.html#schemdraw.logic.timing.TimingDiagram "schemdraw.logic.timing.TimingDiagram") Element in the `schemdraw.logic` module.

Timing diagrams are set up using the WaveJSON syntax used by the [WaveDrom](https://wavedrom.com/) JavaScript application.

from schemdraw import logic

logic.TimingDiagram(
    {'signal': \[
        {'name': 'A', 'wave': '0..1..01.'},
        {'name': 'B', 'wave': '101..0...'}\]})

![_images/timing_1_0.svg](_images/timing_1_0.svg)

The input is a dictionary containing a signal, which is a list of each wave to show in the diagram. Each signal is a dictionary which must contain a name and wave. An empty dictionary leaves a blank row in the diagram.

Every character in the wave specifies the state of the wave for one period. A dot . means the previous state is repeated. Wave characters ‘n’ and ‘p’ specify clock signals, and ‘N’, and ‘P’ draw clocks with arrows. ‘1’ and ‘0’ are used to define high and low signals. ‘2’ draws a data block, and ‘3’ through ‘9’ draw data filled with a color. ‘x’ draws a don’t-care or undefined data state.

Data blocks can be labeled by adding a ‘data’ item to the wave’s dictionary.

This example shows the different wave sections:

logic.TimingDiagram(
    {'signal': \[
        {'name': 'clock n', 'wave': 'n......'},
        {'name': 'clock p', 'wave': 'p......'},
        {'name': 'clock N', 'wave': 'N......'},
        {'name': 'clock P', 'wave': 'P......'},
        {},
        {'name': '1s and 0s', 'wave': '0.1.01.'},
        {'name': 'data', 'wave': '2..=.2.'},  \# '=' is the same as '2'
        {'name': 'data named', 'wave': '3.4.6..', 'data': \['A', 'B', 'C'\]},
        {'name': 'dont care', 'wave': 'xx..x..'},
        {},
        {'name': 'high z', 'wave': 'z.10.z.'},
        {'name': 'pull up/down', 'wave': '0u..d.1'},
    \]})

![_images/timing_2_0.svg](_images/timing_2_0.svg)

Putting them together in a more realistic example:

logic.TimingDiagram(
    {'signal': \[
        {'name': 'clk', 'wave': 'P......'},
        {'name': 'bus', 'wave': 'x.==.=x', 'data': \['head', 'body', 'tail'\]},
        {'name': 'wire', 'wave': '0.1..0.'}\]})

![_images/timing_3_0.svg](_images/timing_3_0.svg)

The config key, containing a dictionary with hscale, may be used to change the width of one period in the diagram:

logic.TimingDiagram(
    {'signal': \[
        {'name': 'clk', 'wave': 'P......'},
        {'name': 'bus', 'wave': 'x.==.=x', 'data': \['head', 'body', 'tail'\]},
        {'name': 'wire', 'wave': '0.1..0.'}\],
     'config': {'hscale': 2}})

![_images/timing_4_0.svg](_images/timing_4_0.svg)

Signals may also be nested into different groups:

logic.TimingDiagram(
    {'signal': \['Group',
      \['Set 1',
        {'name': 'A', 'wave': '0..1..01.'},
        {'name': 'B', 'wave': '101..0...'}\],
      \['Set 2',
        {'name': 'C', 'wave': '0..1..01.'},
        {'name': 'D', 'wave': '101..0...'}\]
               \]})

![_images/timing_5_0.svg](_images/timing_5_0.svg)

Using the node key in a waveform, plus the edge key in the top-level dictionary, provides a way to show transitions between different edges.

logic.TimingDiagram(
    {'signal': \[
        {'name': 'A', 'wave': '0..1..01.', 'node': '...a.....'},
        {'name': 'B', 'wave': '101..0...', 'node': '.....b...'}\],
     'edge': \['a~>b'\]    })

![_images/timing_6_0.svg](_images/timing_6_0.svg)

Each string in the edge list must start and end with a node name (single character). The characters between them define the type of connecting line: ‘-’ for straight line, ‘~’ for curve, ‘-|’ for orthogonal lines, and < or > to include arrowheads. For example, ‘a-~>b’ draws a curved line with arrowhead between nodes a and b.

#### Using JSON[¶](#using-json "Link to this heading")

Because the examples from WaveDrom use JavaScript and JSON, they sometimes cannot be directly pasted into Python as dictionaries. The `schemdraw.logic.timing.TimingDiagram.from_json()` method allows input of the WaveJSON as a string pasted directly from the Javascript/JSON examples without modification.

Notice lack of quoting on the dictionary keys, requiring the from\_json method to parse the string.

logic.TimingDiagram.from\_json('''{ signal: \[
  { name: "clk",  wave: "P......" },
  { name: "bus",  wave: "x.==.=x", data: \["head", "body", "tail", "data"\] },
  { name: "wire", wave: "0.1..0." }
\]}''')

![_images/timing_7_0.svg](_images/timing_7_0.svg)

#### Schemdraw’s Customizations[¶](#schemdraw-s-customizations "Link to this heading")

Schemdraw extends the WaveJSON spcification with a few additional options.

##### Style Parameters[¶](#style-parameters "Link to this heading")

Each wave dictionary accpets a color and lw parameter. The rise/fall time for transitions can be set using the risetime parameter to TimingDiagram. Other colors and font sizes may be speficied using keyword arguments to [`schemdraw.logic.timing.TimingDiagram`](index.html#schemdraw.logic.timing.TimingDiagram "schemdraw.logic.timing.TimingDiagram").

##### Asynchronous Signals[¶](#asynchronous-signals "Link to this heading")

WaveDrom does not have a means for defining asynchronous signals - all waves must transition on period boundaries. Schemdraw adds asyncrhonous signals using the async parameter, as a list of period multiples for each transition in the wave. Note the beginning and end time of the wave must also be specified, so the length of the async list must be one more than the length of wave.

logic.TimingDiagram(
    {'signal': \[
        {'name': 'clk', 'wave': 'n......'},
        {'name': 'B', 'wave': '010', 'async': \[0, 1.6, 4.25, 7\]}\]},    risetime\=.03)

![_images/timing_8_0.svg](_images/timing_8_0.svg)

##### Extended Edge Notation[¶](#extended-edge-notation "Link to this heading")

Additional “edge” string notations are allowed for more complex labeling of edge timings, including asynchronous start and end times and labels just above or below a wave.

Each edge string using this syntax takes the form

'\[WaveNum:Period\]<->\[WaveNum:Period\]{color,ls} Label'

Everything after the first space will be drawn as the label in the center of the line. The values in square brackets designate the start and end position of the line. WaveNum is the integer row number (starting at 0) of the wave, and Period is the possibly fractional number of periods in time for the node. WaveNum may be appended by a ^ or v to designate notations just above, or just below, the wave, respectively.

Between the two square-bracket expressions is the standard line/arrow type designator. In optional curly braces, the line color and linestyle may be entered.

Some examples are shown here:

logic.TimingDiagram(
    {'signal': \[
        {'name': 'A', 'wave': 'x3...x'},
        {'name': 'B', 'wave': 'x6.6.x'}\],
     'edge': \['\[0^:1\]+\[0^:5\] $t\_1$',              '\[1^:1\]<->\[1^:3\] $t\_o$',              '\[0^:3\]-\[1v:3\]{gray,:}',             \]},
    ygap\=.5, grid\=False)

![_images/timing_9_0.svg](_images/timing_9_0.svg)

When placing edge labels above or below the wave, it can be useful to add the ygap parameter to TimingDiagram to increase the spacing between waves.

See the [Timing Diagrams](index.html#gallerytiming) Gallery for more examples.

### Signal Processing[¶](#signal-processing "Link to this heading")

Signal processing elements can be drawn by importing the [`schemdraw.dsp.dsp`](index.html#module-schemdraw.dsp.dsp "schemdraw.dsp.dsp") module:

from schemdraw import dsp

Because each element may have multiple connections in and out, these elements are not 2-terminal elements that extend “leads”, so they must be manually connected with Line or Arrow elements. The square elements define anchors ‘N’, ‘S’, ‘E’, and ‘W’ for the four directions. Circle-based elements also includ ‘NE’, ‘NW’, ‘SE’, and ‘SW’ anchors. Directional elements, such as Amp, Adc, and Dac define anchors input and out.

![_images/dsp_1_0.svg](_images/dsp_1_0.svg)

Labels are placed in the center of the element. The generic Square and Circle elements can be used with a label to define other operations. For example, an integrator may be created using:

dsp.Square().label('$\\int$')

![_images/dsp_2_0.svg](_images/dsp_2_0.svg)

### Flowcharts and Diagrams[¶](#flowcharts-and-diagrams "Link to this heading")

Schemdraw provides basic symbols for flowcharting and state diagrams. The [`schemdraw.flow.flow`](index.html#module-schemdraw.flow.flow "schemdraw.flow.flow") module contains a set of functions for defining flowchart blocks and connecting lines that can be added to schemdraw Drawings.

from schemdraw import flow

Flowchart blocks:

![_images/flow_1_0.svg](_images/flow_1_0.svg)

Some elements have been defined with multiple names, which can be used depending on the context or user preference:

![_images/flow_2_0.svg](_images/flow_2_0.svg)

All flowchart symbols have 16 anchor positions named for the compass directions: ‘N’, ‘S’, ‘E’, ‘W’, ‘NE’, ‘SE, ‘NNE’, etc., plus a ‘center’ anchor.

The [`schemdraw.elements.intcircuits.Ic`](index.html#schemdraw.elements.intcircuits.Ic "schemdraw.elements.intcircuits.Ic") element can be used with the flowchart elements to create blocks with other inputs/outputs per side if needed.

The size of each block must be specified manually using w and h or r parameters to size each block to fit any labels.

#### Connecting Lines[¶](#connecting-lines "Link to this heading")

Typical flowcharts will use Line or Arrow elements to connect the boxes. The line and arrow elements have been included in the flow module for convenience.

with schemdraw.Drawing() as d:
    d.config(fontsize\=10, unit\=.5)
    d += flow.Terminal().label('Start')
    d += flow.Arrow()
    d += flow.Process().label('Do something').drop('E')
    d += flow.Arrow().right()
    d += flow.Process().label('Do something\\nelse')

![_images/flow_3_0.svg](_images/flow_3_0.svg)

Some flow diagrams, such as State Machine diagrams, often use curved connectors between states. Several Arc connectors are available. Each Arc element takes an arrow parameter, which may be ‘->’, ‘<-’, or ‘<->’, to define the end(s) on which to draw arrowheads.

##### Arc2[¶](#arc2 "Link to this heading")

Arc2 draws a symmetric quadratic Bezier curve between the endpoints, with curvature controlled by parameter k. Endpoints of the arc should be specified using at() and to() methods.

d += (a := flow.State().label('A'))
d += (b := flow.State(arrow\='->').label('B').at((4, 0)))
d += flow.Arc2(arrow\='->').at(a.NE).to(b.NW).color('deeppink').label('Arc2')
d += flow.Arc2(k\=.2, arrow\='<->').at(b.SW).to(a.SE).color('mediumblue').label('Arc2')

![_images/flow_6_0.svg](_images/flow_6_0.svg)

##### ArcZ and ArcN[¶](#arcz-and-arcn "Link to this heading")

These draw symmetric cubic Bezier curves between the endpoints. The ArcZ curve approaches the endpoints horizontally, and ArcN approaches them vertically.

d += (a := flow.State().label('A'))
d += (b := flow.State().label('B').at((4, 4)))
d += (c := flow.State().label('C').at((8, 0)))
d += flow.ArcN(arrow\='<->').at(a.N).to(b.S).color('deeppink').label('ArcN')
d += flow.ArcZ(arrow\='<->').at(b.E).to(c.W).color('mediumblue').label('ArcZ')

![_images/flow_9_0.svg](_images/flow_9_0.svg)

##### Arc3[¶](#arc3 "Link to this heading")

The Arc3 curve is an arbitrary cubic Bezier curve, defined by endpoints and angle of approach to each endpoint. ArcZ and ArcN are simply Arc3 defined with the angles as 0 and 180, or 90 and 270, respectively.

d += (a := flow.State().label('A'))
d += (b := flow.State().label('B').at((3, 3)))
d += flow.Arc3(th1\=75, th2\=-45, arrow\='<->').at(a.N).to(b.SE).color('deeppink').label('Arc3')

![_images/flow_12_0.svg](_images/flow_12_0.svg)

##### ArcLoop[¶](#arcloop "Link to this heading")

The ArcLoop curve draws a partial circle that intersects the two endpoints, with the given radius. Often used in state machine diagrams to indicate cases where the state does not change.

d += (a := flow.State().label('A'))
d += flow.ArcLoop(arrow\='<-').at(a.NW).to(a.NNE).color('mediumblue').label('ArcLoop', halign\='center')

![_images/flow_15_0.svg](_images/flow_15_0.svg)

#### Decisions[¶](#decisions "Link to this heading")

To label the decision branches, the [`schemdraw.flow.flow.Decision`](index.html#schemdraw.flow.flow.Decision "schemdraw.flow.flow.Decision") element takes keyword arguments for each cardinal direction. For example:

decision \= flow.Decision(W\='Yes', E\='No', S\='Maybe').label('Question?')

![_images/flow_18_0.svg](_images/flow_18_0.svg)

#### Layout and Flow[¶](#layout-and-flow "Link to this heading")

Without any directions specified, boxes flow top to bottom (see left image). If a direction is specified (right image), the flow will continue in that direction, starting the next arrow at an appropriate anchor. Otherwise, the drop method is useful for specifing where to begin the next arrow.

with schemdraw.Drawing() as d:
    d.config(fontsize\=10, unit\=.5)
    d += flow.Terminal().label('Start')
    d += flow.Arrow()
    d += flow.Process().label('Step 1')
    d += flow.Arrow()
    d += flow.Process().label('Step 2').drop('E')
    d += flow.Arrow().right()
    d += flow.Connect().label('Next')

    d += flow.Terminal().label('Start').at((4, 0))
    d += flow.Arrow().theta(\-45)
    d += flow.Process().label('Step 1')
    d += flow.Arrow()
    d += flow.Process().label('Step 2').drop('E')
    d += flow.Arrow().right()
    d += flow.Connect().label('Next')

![_images/flow_19_0.svg](_images/flow_19_0.svg)

See the [Flowcharting](index.html#galleryflow) Gallery for more examples.

Circuit Gallery[¶](#circuit-gallery "Link to this heading")
-----------------------------------------------------------

### Analog Circuits[¶](#analog-circuits "Link to this heading")

#### Discharging capacitor[¶](#discharging-capacitor "Link to this heading")

Shows how to connect to a switch with anchors.

![_images/analog_1_0.svg](_images/analog_1_0.svg)

with schemdraw.Drawing() as d:
    d += (V1 := elm.SourceV().label('5V'))
    d += elm.Line().right(d.unit\*.75)
    d += (S1 := elm.SwitchSpdt2(action\='close').up().anchor('b').label('$t=0$', loc\='rgt'))
    d += elm.Line().right(d.unit\*.75).at(S1.c)
    d += elm.Resistor().down().label('$100\\Omega$').label(\['+','$v\_o$','-'\], loc\='bot')
    d += elm.Line().to(V1.start)
    d += elm.Capacitor().at(S1.a).toy(V1.start).label('1$\\mu$F').dot()

#### Capacitor Network[¶](#capacitor-network "Link to this heading")

Shows how to use endpoints to specify exact start and end placement.

![_images/analog_2_0.svg](_images/analog_2_0.svg)

with schemdraw.Drawing() as d:
    d.config(fontsize\=12)
    d += (C1 := elm.Capacitor().label('8nF').idot().label('a', 'left'))
    d += (C2 := elm.Capacitor().label('18nF'))
    d += (C3 := elm.Capacitor().down().label('8nF', loc\='bottom'))
    d += (C4 := elm.Capacitor().left().label('32nF'))
    d += (C5 := elm.Capacitor().label('40nF', loc\='bottom').dot().label('b', 'left'))
    d += (C6 := elm.Capacitor().endpoints(C1.end, C5.start).label('2.8nF'))
    d += (C7 := elm.Capacitor().endpoints(C2.end, C5.start)
          .label('5.6nF', loc\='center', ofst\=(\-.3, \-.1), halign\='right', valign\='bottom'))

#### ECE201-Style Circuit[¶](#ece201-style-circuit "Link to this heading")

This example demonstrate use of push() and pop() and using the ‘tox’ and ‘toy’ methods.

![_images/analog_3_0.svg](_images/analog_3_0.svg)

with schemdraw.Drawing() as d:
    d.config(unit\=2)  \# unit=2 makes elements have shorter than normal leads
    d.push()
    d += (R1 := elm.Resistor().down().label('20Ω'))
    d += (V1 := elm.SourceV().down().reverse().label('120V'))
    d += elm.Line().right(3).dot()
    d.pop()
    d += elm.Line().right(3).dot()
    d += elm.SourceV().down().reverse().label('60V')
    d += elm.Resistor().label('5Ω').dot()
    d += elm.Line().right(3).dot()
    d += elm.SourceI().up().label('36A')
    d += elm.Resistor().label('10Ω').dot()
    d += elm.Line().left(3).hold()
    d += elm.Line().right(3).dot()
    d += (R6 := elm.Resistor().toy(V1.end).label('6Ω').dot())
    d += elm.Line().left(3).hold()
    d += elm.Resistor().right().at(R6.start).label('1.6Ω').dot(open\=True).label('a', 'right')
    d += elm.Line().right().at(R6.end).dot(open\=True).label('b', 'right')

#### Loop Currents[¶](#loop-currents "Link to this heading")

Using the [`schemdraw.elements.lines.LoopCurrent`](index.html#schemdraw.elements.lines.LoopCurrent "schemdraw.elements.lines.LoopCurrent") element to add loop currents, and rotating a label to make it fit.

![_images/analog_4_0.svg](_images/analog_4_0.svg)

with schemdraw.Drawing() as d:
    d.config(unit\=5)
    d += (V1 := elm.SourceV().label('20V'))
    d += (R1 := elm.Resistor().right().label('400Ω'))
    d += elm.Dot()
    d.push()
    d += (R2 := elm.Resistor().down().label('100Ω', loc\='bot', rotate\=True))
    d += elm.Dot()
    d.pop()
    d += (L1 := elm.Line())
    d += (I1 := elm.SourceI().down().label('1A', loc\='bot'))
    d += (L2 := elm.Line().tox(V1.start))
    d += elm.LoopCurrent(\[R1,R2,L2,V1\], pad\=1.25).label('$I\_1$')
    d += elm.LoopCurrent(\[R1,I1,L2,R2\], pad\=1.25).label('$I\_2$')    \# Use R1 as top element for both so they get the same height

#### AC Loop Analysis[¶](#ac-loop-analysis "Link to this heading")

Another good problem for ECE students…

![_images/analog_5_0.svg](_images/analog_5_0.svg)

with schemdraw.Drawing() as d:
    d += (I1 := elm.SourceI().label('5∠0° A').dot())
    d.push()
    d += elm.Capacitor().right().label('-j3Ω').dot()
    d += elm.Inductor().down().label('j2Ω').dot().hold()
    d += elm.Resistor().right().label('5Ω').dot()
    d += (V1 := elm.SourceV().down().reverse().label('5∠-90° V', loc\='bot'))
    d += elm.Line().tox(I1.start)
    d.pop()
    d += elm.Line().up(d.unit\*.8)
    d += (L1 := elm.Inductor().tox(V1.start).label('j3Ω'))
    d += elm.Line().down(d.unit\*.8)
    d += elm.CurrentLabel(top\=False, ofst\=.3).at(L1).label('$i\_g$')

#### Infinite Transmission Line[¶](#infinite-transmission-line "Link to this heading")

Elements can be added inside for-loops if you need multiples. The ellipsis is just another circuit element, called DotDotDot since Ellipsis is a reserved keyword in Python. This also demonstrates the [`schemdraw.elements.ElementDrawing`](index.html#schemdraw.elements.ElementDrawing "schemdraw.elements.ElementDrawing") class to merge multiple elements into a single definition.

![_images/analog_6_0.svg](_images/analog_6_0.svg)

with schemdraw.Drawing(show\=False) as d1:
    d1 += elm.Resistor()
    d1.push()
    d1 += elm.Capacitor().down()
    d1 += elm.Line().left()
    d1.pop()

with schemdraw.Drawing() as d2:
    for i in range(3):
        d2 += elm.ElementDrawing(d1)

    d2.push()
    d2 += elm.Line().length(d2.unit/6)
    d2 += elm.DotDotDot()
    d2 += elm.ElementDrawing(d1)
    d2.pop()
    d2.here \= (d2.here\[0\], d2.here\[1\]\-d2.unit)
    d2 += elm.Line().right().length(d2.unit/6)
    d2 += elm.DotDotDot()

#### Power supply[¶](#power-supply "Link to this heading")

Notice the diodes could be added individually, but here the built-in Rectifier element is used instead. Also note the use of newline characters inside resistor and capacitor labels.

![_images/analog_7_0.svg](_images/analog_7_0.svg)

with schemdraw.Drawing() as d:
    d.config(inches\_per\_unit\=.5, unit\=3)
    d += (D := elm.Rectifier())
    d += elm.Line().left(d.unit\*1.5).at(D.N).dot(open\=True).idot()
    d += elm.Line().left(d.unit\*1.5).at(D.S).dot(open\=True).idot()
    d += (G := elm.Gap().toy(D.N).label(\['–', 'AC IN', '+'\]))

    d += (top := elm.Line().right(d.unit\*3).at(D.E).idot())
    d += (Q2 := elm.BjtNpn(circle\=True).up().anchor('collector').label('Q2\\n2n3055'))
    d += elm.Line().down(d.unit/2).at(Q2.base)
    d += (Q2b := elm.Dot())
    d += elm.Line().left(d.unit/3)
    d += (Q1 := elm.BjtNpn(circle\=True).up().anchor('emitter').label('Q1\\n    2n3054'))
    d += elm.Line().at(Q1.collector).toy(top.center).dot()

    d += elm.Line().down(d.unit/2).at(Q1.base).dot()
    d += elm.Zener().down().reverse().label('D2\\n500mA', loc\='bot').dot()
    d += (G := elm.Ground())
    d += elm.Line().left().dot()
    d += elm.Capacitor(polar\=True).up().reverse().label('C2\\n100$\\mu$F\\n50V', loc\='bot').dot()
    d += elm.Line().right().hold()
    d += elm.Resistor().toy(top.end).label('R1\\n2.2K\\n50V', loc\='bot').dot()

    d.move(dx\=-d.unit, dy\=0)
    d += elm.Capacitor(polar\=True).toy(G.start).flip().label('C1\\n 1000$\\mu$F\\n50V').dot().idot()
    d += elm.Line().at(G.start).tox(D.W)
    d += elm.Line().toy(D.W).dot()

    d += elm.Resistor().right().at(Q2b.center).label('R2').label('56$\\Omega$ 1W', loc\='bot').dot()
    d.push()
    d += elm.Line().toy(top.start).dot()
    d += elm.Line().tox(Q2.emitter)
    d.pop()
    d += elm.Capacitor(polar\=True).toy(G.start).label('C3\\n470$\\mu$F\\n50V', loc\='bot').dot()
    d += elm.Line().tox(G.start).hold()
    d += elm.Line().right().dot()
    d += elm.Resistor().toy(top.center).label('R3\\n10K\\n1W', loc\='bot').dot()
    d += elm.Line().left().hold()
    d += elm.Line().right()
    d += elm.Dot(open\=True)
    d += elm.Gap().toy(G.start).label(\['+', '$V\_{out}$', '–'\])
    d += elm.Dot(open\=True)
    d += elm.Line().left()

#### 5-transistor Operational Transconductance Amplifer (OTA)[¶](#transistor-operational-transconductance-amplifer-ota "Link to this heading")

Note the use of current labels to show the bias currents.

![_images/analog_8_0.svg](_images/analog_8_0.svg)

with schemdraw.Drawing() as d:
    \# tail transistor
    d += (Q1 := elm.AnalogNFet()).anchor('source').theta(0).reverse()
    d += elm.Line().down().length(0.5)
    ground \= d.here
    d += elm.Ground()

    \# input pair
    d += elm.Line().left().length(1).at(Q1.drain)
    d += (Q2 := elm.AnalogNFet()).anchor('source').theta(0).reverse()

    d += elm.Dot().at(Q1.drain)
    d += elm.Line().right().length(1)
    d += (Q3 := elm.AnalogNFet()).anchor('source').theta(0)

    \# current mirror
    d += (Q4 := elm.AnalogPFet()).anchor('drain').at(Q2.drain).theta(0)
    d += (Q5 := elm.AnalogPFet()).anchor('drain').at(Q3.drain).theta(0).reverse()

    d += elm.Line().right().at(Q4.gate).to(Q5.gate)

    d += elm.Dot().at(0.5\*(Q4.gate + Q5.gate))
    d += elm.Line().down().toy(Q4.drain)
    d += elm.Line().left().tox(Q4.drain)
    d += elm.Dot()

    \# vcc connection
    d += elm.Line().right().at(Q4.source).to(Q5.source)
    d += elm.Dot().at(0.5\*(Q4.source + Q5.source))
    d += elm.Vdd()

    \# bias source
    d += elm.Line().left().length(0.25).at(Q1.gate)
    d += elm.SourceV().down().toy(ground).reverse().scale(0.5).label("Bias")
    d += elm.Ground()

    \# signal labels
    d += elm.Tag().at(Q2.gate).label("In+").left()
    d += elm.Tag().at(Q3.gate).label("In−").right()
    d += elm.Dot().at(Q3.drain)
    d += elm.Line().right().tox(Q3.gate)
    d += elm.Tag().right().label("Out").reverse()

    \# bias currents
    d += elm.CurrentLabel(length\=1.25, ofst\=0.25).at(Q1).label("20µA")
    d += elm.CurrentLabel(length\=1.25, ofst\=0.25).at(Q4).label("10µA")
    d += elm.CurrentLabel(length\=1.25, ofst\=0.25).at(Q5).label("10µA")

#### Quadruple loop negative feedback amplifier[¶](#quadruple-loop-negative-feedback-amplifier "Link to this heading")

![_images/analog_9_0.svg](_images/analog_9_0.svg)

with schemdraw.Drawing() as d:
    \# place twoports
    d += (N1 := elm.Nullor()).anchor('center')
    d += (T1 := elm.TransimpedanceTransactor(reverse\_output\=True)).reverse().flip().anchor('center').at(\[0,\-3\]).label("B")
    d += (T2 := elm.CurrentTransactor()).reverse().flip().anchor('center').at(\[0,\-6\]).label("D")
    d += (T3 := elm.VoltageTransactor()).reverse().anchor('center').at(\[0,\-9\]).label("A")
    d += (T4 := elm.TransadmittanceTransactor(reverse\_output\=True)).reverse().anchor('center').at(\[0,\-12\]).label("C")

    \## make connections
    \# right side
    d += elm.Line().at(N1.out\_n).to(T1.in\_n)
    d += elm.Line().at(T1.in\_p).to(T2.in\_n)
    d += elm.Line().at(T3.in\_n).to(T4.in\_n)

    d += elm.Line().right().length(1).at(N1.out\_p)
    pre\_out \= d.here
    d += (outline := elm.Line()).right().length(1).dot(open\=True)
    out \= d.here
    d += elm.Gap().down().label(('+','$V\_o$','–')).toy(N1.out\_n)
    d += elm.Line().idot(open\=True).down().toy(T4.in\_n)
    d += elm.Line().left().to(T4.in\_n)
    d += elm.Dot()
    d += elm.CurrentLabelInline(direction\='in', ofst\=-0.15).at(outline).label('$I\_o$')

    d += elm.Line().at(T2.in\_p).right().tox(out)
    d += elm.Dot()

    d += elm.Line().right().at(T4.in\_p).tox(pre\_out)
    d += elm.Line().up().toy(pre\_out)
    d += elm.Dot()

    d += elm.Line().right().at(T3.in\_p).tox(pre\_out)
    d += elm.Dot()

    \# left side
    d += elm.Line().down().at(N1.in\_n).to(T1.out\_n)

    d += elm.Line().up().at(T3.out\_p).to(T1.out\_p)

    d += elm.Line().left().at(N1.in\_p).length(1)
    pre\_in \= d.here
    d += (inline := elm.Line()).length(1).dot(open\=True).left()
    in\_node \= d.here
    d += elm.Gap().down().label(('+','$V\_i$','–')).toy(N1.in\_n)
    d += elm.Line().idot(open\=True).down().toy(T4.out\_n)
    d += elm.Line().right().to(T4.out\_n)
    d += elm.CurrentLabelInline(direction\='out', ofst\=-0.15).at(inline).label('$I\_i$')

    d += elm.Line().left().at(T2.out\_p).tox(in\_node)
    d += elm.Dot()
    d += elm.Line().left().at(T3.out\_n).tox(in\_node)
    d += elm.Dot()

    d += elm.Line().left().at(T4.out\_p).tox(pre\_in)
    d += elm.Line().up().toy(pre\_in)
    d += elm.Dot()

    d += elm.Line().left().at(T2.out\_n).tox(pre\_in)
    d += elm.Dot()

### Opamp Circuits[¶](#opamp-circuits "Link to this heading")

#### Inverting Opamp[¶](#inverting-opamp "Link to this heading")

![_images/opamp_1_0.svg](_images/opamp_1_0.svg)

with schemdraw.Drawing() as d:
    d += (op := elm.Opamp(leads\=True))
    d += elm.Line().down(d.unit/4).at(op.in2)
    d += elm.Ground(lead\=False)
    d += (Rin := elm.Resistor().at(op.in1).left().idot().label('$R\_{in}$', loc\='bot').label('$v\_{in}$', loc\='left'))
    d += elm.Line().up(d.unit/2).at(op.in1)
    d += elm.Resistor().tox(op.out).label('$R\_f$')
    d += elm.Line().toy(op.out).dot()
    d += elm.Line().right(d.unit/4).at(op.out).label('$v\_{o}$', loc\='right')

#### Non-inverting Opamp[¶](#non-inverting-opamp "Link to this heading")

![_images/opamp_2_0.svg](_images/opamp_2_0.svg)

with schemdraw.Drawing() as d:
    d += (op := elm.Opamp(leads\=True))
    d += (out := elm.Line(at\=op.out).length(.75))
    d += elm.Line().up().at(op.in1).length(1.5).dot()
    d.push()
    d += elm.Resistor().left().label('$R\_1$')
    d += elm.Ground()
    d.pop()
    d += elm.Resistor().tox(op.out).label('$R\_f$')
    d += elm.Line().toy(op.out).dot()
    d += elm.Resistor().left().at(op.in2).idot().label('$R\_2$')
    d += elm.SourceV().down().reverse().label('$v\_{in}$')
    d += elm.Line().right().dot()
    d += elm.Resistor().up().label('$R\_3$').hold()
    d += elm.Line().tox(out.end)
    d += elm.Gap().toy(op.out).label(\['–','$v\_o$','+'\])

#### Multi-stage amplifier[¶](#multi-stage-amplifier "Link to this heading")

![_images/opamp_3_0.svg](_images/opamp_3_0.svg)

with schemdraw.Drawing() as d:
    d += elm.Ground(lead\=False)
    d += elm.SourceV().label('500mV')
    d += elm.Resistor().right().label('20k$\\Omega$').dot()
    d += (O1 := elm.Opamp(leads\=True).anchor('in1'))
    d += elm.Ground().at(O1.in2)
    d += elm.Line().up(2).at(O1.in1)
    d += elm.Resistor().tox(O1.out).label('100k$\\Omega$')
    d += elm.Line().toy(O1.out).dot()
    d += elm.Line().right(5).at(O1.out)
    d += (O2 := elm.Opamp(leads\=True).anchor('in2'))
    d += elm.Resistor().left().at(O2.in1).idot().label('30k$\\Omega$')
    d += elm.Ground()
    d += elm.Line().up(1.5).at(O2.in1)
    d += elm.Resistor().tox(O2.out).label('90k$\\Omega$')
    d += elm.Line().toy(O2.out).dot()
    d += elm.Line().right(1).at(O2.out).label('$v\_{out}$', loc\='rgt')

#### Opamp pin labeling[¶](#opamp-pin-labeling "Link to this heading")

This example shows how to label pin numbers on a 741 opamp, and connect to the offset anchors. Pin labels are somewhat manually placed; without the ofst and align keywords they will be drawn directly over the anchor position.

![_images/opamp_4_0.svg](_images/opamp_4_0.svg)

with schemdraw.Drawing() as d:
    d.config(fontsize\=12)
    op \= (elm.Opamp().label('741', loc\='center', ofst\=0)
                 .label('1', 'n1', fontsize\=9, ofst\=(\-.1, \-.25), halign\='right', valign\='top')
                 .label('5', 'n1a', fontsize\=9, ofst\=(\-.1, \-.25), halign\='right', valign\='top')
                 .label('4', 'vs', fontsize\=9, ofst\=(\-.1, \-.2), halign\='right', valign\='top')
                 .label('7', 'vd', fontsize\=9, ofst\=(\-.1, .2), halign\='right', valign\='bottom')
                 .label('2', 'in1', fontsize\=9, ofst\=(\-.1, .1), halign\='right', valign\='bottom')
                 .label('3', 'in2', fontsize\=9, ofst\=(\-.1, .1), halign\='right', valign\='bottom')
                 .label('6', 'out', fontsize\=9, ofst\=(\-.1, .1), halign\='left', valign\='bottom'))
    d += op
    d += elm.Line().left(.5).at(op.in1)
    d += elm.Line().down(d.unit/2)
    d += elm.Ground(lead\=False)
    d += elm.Line().left(.5).at(op.in2)
    d += elm.Line().right(.5).at(op.out).label('$V\_o$', 'right')
    d += elm.Line().up(1).at(op.vd).label('$+V\_s$', 'right')
    d += (trim := elm.Potentiometer().down().at(op.n1).flip().scale(0.7))
    d += elm.Line().tox(op.n1a)
    d += elm.Line().up().to(op.n1a)
    d += elm.Line().at(trim.tap).tox(op.vs).dot()
    d.push()
    d += elm.Line().down(d.unit/3)
    d += elm.Ground()
    d.pop()
    d += elm.Line().toy(op.vs)

#### Triaxial Cable Driver[¶](#triaxial-cable-driver "Link to this heading")

![_images/opamp_5_0.svg](_images/opamp_5_0.svg)

with schemdraw.Drawing() as d:
    d.config(fontsize\=10)
    d += elm.Line().length(d.unit/5).label('V', 'left')
    d += (smu := elm.Opamp(sign\=False).anchor('in2')
                      .label('SMU', 'center', ofst\=\[\-.4, 0\], halign\='center', valign\='center'))
    d += elm.Line().at(smu.out).length(.3)
    d.push()
    d += elm.Line().length(d.unit/4)
    d += (triax := elm.Triax(length\=5, shieldofststart\=.75))
    d.pop()
    d += elm.Resistor().up().scale(0.6).idot()
    d += elm.Line().left().dot()
    d += elm.Wire('|-').to(smu.in1).hold()
    d += elm.Wire('|-').delta(d.unit/5, d.unit/5)
    d += (buf := elm.Opamp(sign\=False).anchor('in2').scale(0.6)
                         .label('BUF', 'center', ofst\=(\-.4, 0), halign\='center', valign\='center'))

    d += elm.Line().left(d.unit/5).at(buf.in1)
    d += elm.Wire('n').to(buf.out, dx\=.5).dot()
    d += elm.Wire('-|').at(buf.out).to(triax.guardstart\_top)
    d += elm.GroundChassis().at(triax.shieldcenter)

### Digital Logic[¶](#digital-logic "Link to this heading")

Logic gate definitions are in the [`schemdraw.logic.logic`](index.html#module-schemdraw.logic.logic "schemdraw.logic.logic") module. Here it was imported with

from schemdraw import logic

#### Half Adder[¶](#half-adder "Link to this heading")

Notice the half and full adders set the drawing unit to 0.5 so the lines aren’t quite as long and look better with logic gates.

![_images/logicgate_1_0.svg](_images/logicgate_1_0.svg)

with schemdraw.Drawing() as d:
    d.config(unit\=0.5)
    d += (S := logic.Xor().label('S', 'right'))
    d += logic.Line().left(d.unit\*2).at(S.in1).idot().label('A', 'left')
    d += (B := logic.Line().left().at(S.in2).dot())
    d += logic.Line().left().label('B', 'left')
    d += logic.Line().down(d.unit\*3).at(S.in1)
    d += (C := logic.And().right().anchor('in1').label('C', 'right'))
    d += logic.Wire('|-').at(B.end).to(C.in2)

#### Full Adder[¶](#full-adder "Link to this heading")

![_images/logicgate_2_0.svg](_images/logicgate_2_0.svg)

with schemdraw.Drawing() as d:
    d.config(unit\=0.5)
    d += (X1 := logic.Xor())
    d += (A := logic.Line().left(d.unit\*2).at(X1.in1).idot().label('A', 'left'))
    d += (B := logic.Line().left().at(X1.in2).dot())
    d += logic.Line().left().label('B', 'left')

    d += logic.Line().right().at(X1.out).idot()
    d += (X2 := logic.Xor().anchor('in1'))
    d += (C := logic.Line().down(d.unit\*2).at(X2.in2))
    d.push()
    d += logic.Dot().at(C.center)
    d += logic.Line().tox(A.end).label('C$\_{in}$', 'left')
    d.pop()

    d += (A1 := logic.And().right().anchor('in1'))
    d += logic.Wire('-|').at(A1.in2).to(X1.out)
    d.move\_from(A1.in2, dy\=-d.unit\*2)
    d += (A2 := logic.And().right().anchor('in1'))
    d += logic.Wire('-|').at(A2.in1).to(A.start)
    d += logic.Wire('-|').at(A2.in2).to(B.end)
    d.move\_from(A1.out, dy\=-(A1.out.y\-A2.out.y)/2)
    d += (O1 := logic.Or().right().label('C$\_{out}$', 'right'))
    d += logic.Line().at(A1.out).toy(O1.in1)
    d += logic.Line().at(A2.out).toy(O1.in2)
    d += logic.Line().at(X2.out).tox(O1.out).label('S', 'right')

#### J-K Flip Flop[¶](#j-k-flip-flop "Link to this heading")

Note the use of the LaTeX command **overline{Q}** in the label to draw a bar over the inverting output label.

![_images/logicgate_3_0.svg](_images/logicgate_3_0.svg)

with schemdraw.Drawing() as d:
    \# Two front gates (SR latch)
    d += (G1 := logic.Nand(leadout\=.75).anchor('in1'))
    d += logic.Line().length(d.unit/2).label('Q', 'right')
    d.move\_from(G1.in1, dy\=-2.5)
    d += (G2 := logic.Nand(leadout\=.75).anchor('in1'))
    d += logic.Line().length(d.unit/2).label('$\\overline{Q}$', 'right')
    d += logic.Wire('N', k\=.5).at(G2.in1).to(G1.out).dot()
    d += logic.Wire('N', k\=.5).at(G1.in2).to(G2.out).dot()

    \# Two back gates
    d += logic.Line().left(d.unit/6).at(G1.in1)
    d += (J := logic.Nand(inputs\=3).anchor('out').right())
    d += logic.Wire('n', k\=.5).at(J.in1).to(G2.out, dx\=1).dot()
    d += logic.Line().left(d.unit/4).at(J.in2).label('J', 'left')
    d += logic.Line().left(d.unit/6).at(G2.in2)
    d += (K := logic.Nand(inputs\=3).right().anchor('out'))
    d += logic.Wire('n', k\=-.5).at(K.in3).to(G1.out, dx\=.5).dot()
    d += logic.Line().left(d.unit/4).at(K.in2).label('K', 'left')
    d += (C := logic.Line().at(J.in3).toy(K.in1))
    d += logic.Dot().at(C.center)
    d += logic.Line().left(d.unit/4).label('CLK', 'left')

#### S-R Latch (Gates)[¶](#s-r-latch-gates "Link to this heading")

![_images/logicgate_4_0.svg](_images/logicgate_4_0.svg)

with schemdraw.Drawing() as d:
    d += (g1 := logic.Nor())
    d.move\_from(g1.in1, dy\=-2.5)
    d += (g2 := logic.Nor().anchor('in1'))
    d += (g1out := logic.Line().right(.25).at(g1.out))
    d += logic.Wire('N', k\=.5).at(g2.in1).to(g1out.end).dot()
    d += (g2out := logic.Line().right(.25).at(g2.out))
    d += logic.Wire('N', k\=.5).at(g1.in2).to(g2out.end).dot()
    d += logic.Line().at(g1.in1).left(.5).label('R', 'left')
    d += logic.Line().at(g2.in2).left(.5).label('S', 'left')
    d += logic.Line().at(g1.out).right(.75).label('Q', 'right')
    d += logic.Line().at(g2.out).right(.75).label('$\\overline{Q}$', 'right')

### Timing Diagrams[¶](#timing-diagrams "Link to this heading")

Timing diagrams, based on [WaveDrom](https://wavedrom.com/), are drawn using the [`schemdraw.logic.timing.TimingDiagram`](index.html#schemdraw.logic.timing.TimingDiagram "schemdraw.logic.timing.TimingDiagram") class.

from schemdraw import logic

#### SRAM read/write cycle[¶](#sram-read-write-cycle "Link to this heading")

The SRAM examples make use of Schemdraw’s extended ‘edge’ notation for labeling timings just above and below the wave.

![_images/timing_1_01.svg](_images/timing_1_01.svg)

logic.TimingDiagram(
    {'signal': \[
        {'name': 'Address',     'wave': 'x4......x.', 'data': \['Valid address'\]},
        {'name': 'Chip Select', 'wave': '1.0.....1.'},
        {'name': 'Out Enable',  'wave': '1.0.....1.'},
        {'name': 'Data Out',    'wave': 'z...x6...z', 'data': \['Valid data'\]},
    \],
     'edge': \['\[0^:1.2\]+\[0^:8\] $t\_{WC}$',
              '\[0v:1\]+\[0v:5\] $t\_{AQ}$',
              '\[1:2\]+\[1:5\] $t\_{EQ}$',
              '\[2:2\]+\[2:5\] $t\_{GQ}$',
              '\[0^:5\]-\[3v:5\]{lightgray,:}',
             \]
    }, ygap\=.5, grid\=False)

![_images/timing_2_01.svg](_images/timing_2_01.svg)

logic.TimingDiagram(
    {'signal': \[
        {'name': 'Address',      'wave': 'x4......x.', 'data': \['Valid address'\]},
        {'name': 'Chip Select',  'wave': '1.0......1'},
        {'name': 'Write Enable', 'wave': '1..0...1..'},
        {'name': 'Data In',      'wave': 'x...5....x', 'data': \['Valid data'\]},
    \],
     'edge': \['\[0^:1\]+\[0^:8\] $t\_{WC}$',
              '\[2:1\]+\[2:3\] $t\_{SA}$',
              '\[3^:4\]+\[3^:7\] $t\_{WD}$',
              '\[3^:7\]+\[3^:9\] $t\_{HD}$',
              '\[0^:1\]-\[2:1\]{lightgray,:}'\],
    }, ygap\=.4, grid\=False)

#### J-K Flip Flop[¶](#j-k-flip-flop "Link to this heading")

Timing diagram for a J-K flip flop taken from [here](https://commons.wikimedia.org/wiki/File:JK_timing_diagram.svg). Notice the use of the async dictionary parameter on the J and K signals, and the color parameters for the output signals.

![_images/timing_3_01.svg](_images/timing_3_01.svg)

logic.TimingDiagram(
    {'signal': \[
        {'name': 'clk', 'wave': 'P......'},
        {'name': 'J', 'wave': '0101', 'async': \[0, .8, 1.3, 3.7, 7\]},
        {'name': 'K', 'wave': '010101', 'async': \[0, 1.2, 2.3, 2.8, 3.2, 3.7, 7\]},
        {'name': 'Q', 'wave': '010.101', 'color': 'red', 'lw': 1.5},
        {'name': '$\\overline{Q}$', 'wave': '101.010', 'color': 'blue', 'lw': 1.5}\],
    'config': {'hscale': 1.5}}, risetime\=.05)

#### Tutorial Examples[¶](#tutorial-examples "Link to this heading")

These examples were copied from [WaveDrom Tutorial](https://wavedrom.com/tutorial.html). They use the from\_json class method so the examples can be pasted directly as a string. Otherwise, the setup must be converted to a proper Python dictionary.

![_images/timing_4_01.svg](_images/timing_4_01.svg)

logic.TimingDiagram.from\_json('''{ signal: \[{ name: "Alfa", wave: "01.zx=ud.23.456789" }\] }''')

![_images/timing_5_01.svg](_images/timing_5_01.svg)

logic.TimingDiagram.from\_json('''{ signal: \[
  { name: "clk",         wave: "p.....|..." },
  { name: "Data",        wave: "x.345x|=.x", data: \["head", "body", "tail", "data"\] },
  { name: "Request",     wave: "0.1..0|1.0" },
  {},
  { name: "Acknowledge", wave: "1.....|01." }
  \]}''')

### Solid State[¶](#solid-state "Link to this heading")

#### S-R Latch (Transistors)[¶](#s-r-latch-transistors "Link to this heading")

![_images/solidstate_1_0.svg](_images/solidstate_1_0.svg)

with schemdraw.Drawing() as d:
    d += (Q1 := elm.BjtNpn(circle\=True).reverse().label('Q1', 'left'))
    d += (Q2 := elm.BjtNpn(circle\=True).at((d.unit\*2, 0)).label('Q2'))
    d += elm.Line().up(d.unit/2).at(Q1.collector)

    d += (R1 := elm.Resistor().up().label('R1').hold())
    d += elm.Dot().label('V1', 'left')
    d += elm.Resistor().right(d.unit\*.75).label('R3', 'bottom').dot()
    d += elm.Line().up(d.unit/8).dot(open\=True).label('Set', 'right').hold()
    d += elm.Line().to(Q2.base)

    d += elm.Line().up(d.unit/2).at(Q2.collector)
    d += elm.Dot().label('V2', 'right')
    d += (R2 := elm.Resistor().up().label('R2', 'bottom').hold())
    d += elm.Resistor().left(d.unit\*.75).label('R4', 'bottom').dot()
    d += elm.Line().up(d.unit/8).dot(open\=True).label('Reset', 'right').hold()
    d += elm.Line().to(Q1.base)

    d += elm.Line().down(d.unit/4).at(Q1.emitter)
    d += (BOT := elm.Line().tox(Q2.emitter))
    d += elm.Line().to(Q2.emitter)
    d += elm.Dot().at(BOT.center)
    d += elm.Ground().at(BOT.center)

    d += (TOP := elm.Line().endpoints(R1.end, R2.end))
    d += elm.Dot().at(TOP.center)
    d += elm.Vdd().at(TOP.center).label('+Vcc')

#### 741 Opamp Internal Schematic[¶](#opamp-internal-schematic "Link to this heading")

![_images/solidstate_2_0.svg](_images/solidstate_2_0.svg)

with schemdraw.Drawing() as d:
    d.config(fontsize\=12, unit\=2.5)
    d += (Q1 := elm.BjtNpn().label('Q1').label('+IN', 'left'))
    d += (Q3 := elm.BjtPnp().left().at(Q1.emitter).anchor('emitter').flip().label('Q3', 'left'))
    d += elm.Line().down().at(Q3.collector).dot()
    d.push()
    d += elm.Line().right(d.unit/4)
    d += (Q7 := elm.BjtNpn().anchor('base').label('Q7'))
    d.pop()
    d += elm.Line().down(d.unit\*1.25)
    d += (Q5 := elm.BjtNpn().left().flip().anchor('collector').label('Q5', 'left'))
    d += elm.Line().left(d.unit/2).at(Q5.emitter).label('OFST\\nNULL', 'left').flip()
    d += elm.Resistor().down().at(Q5.emitter).label('R1\\n1K')
    d += elm.Line().right(d.unit\*.75).dot()
    d += (R3 := elm.Resistor().up().label('R3\\n50K'))
    d += elm.Line().toy(Q5.base).dot()
    d.push()
    d += elm.Line().left().to(Q5.base)
    d += elm.Line().at(Q7.emitter).toy(Q5.base).dot()
    d.pop()
    d += elm.Line().right(d.unit/4)
    d += (Q6 := elm.BjtNpn().anchor('base').label('Q6'))
    d += elm.Line().at(Q6.emitter).length(d.unit/3).label('\\nOFST\\nNULL', 'right').hold()
    d += elm.Resistor().down().at(Q6.emitter).label('R2\\n1K').dot()

    d += elm.Line().at(Q6.collector).toy(Q3.collector)
    d += (Q4 := elm.BjtPnp().right().anchor('collector').label('Q4'))
    d += elm.Line().at(Q4.base).tox(Q3.base)
    d += elm.Line().at(Q4.emitter).toy(Q1.emitter)
    d += (Q2 := elm.BjtNpn().left().flip().anchor('emitter').label('Q2', 'left').label('$-$IN', 'right'))
    d += elm.Line().up(d.unit/3).at(Q2.collector).dot()
    d += (Q8 := elm.BjtPnp().left().flip().anchor('base').label('Q8', 'left'))
    d += elm.Line().at(Q8.collector).toy(Q2.collector).dot()
    d += elm.Line().at(Q2.collector).tox(Q1.collector)
    d += elm.Line().up(d.unit/4).at(Q8.emitter)
    d += (top := elm.Line().tox(Q7.collector))
    d += elm.Line().toy(Q7.collector)

    d += elm.Line().right(d.unit\*2).at(top.start)
    d += elm.Line().down(d.unit/4)
    d += (Q9 := elm.BjtPnp().right().anchor('emitter').label('Q9', ofst\=-.1))
    d += elm.Line().at(Q9.base).tox(Q8.base)
    d += elm.Dot().at(Q4.base)
    d += elm.Line().down(d.unit/2).at(Q4.base)
    d += elm.Line().tox(Q9.collector).dot()
    d += elm.Line().at(Q9.collector).toy(Q6.collector)
    d += (Q10 := elm.BjtNpn().left().flip().anchor('collector').label('Q10', 'left'))
    d += elm.Resistor().at(Q10.emitter).toy(R3.start).label('R4\\n5K').dot()

    d += (Q11 := elm.BjtNpn().right().at(Q10.base).anchor('base').label('Q11'))
    d += elm.Dot().at(Q11.base)
    d += elm.Line().up(d.unit/2)
    d += elm.Line().tox(Q11.collector).dot()
    d += elm.Line().at(Q11.emitter).toy(R3.start).dot()
    d += elm.Line().up(d.unit\*2).at(Q11.collector)
    d += elm.Resistor().toy(Q9.collector).label('R5\\n39K')
    d += (Q12 := elm.BjtPnp().left().flip().anchor('collector').label('Q12', 'left', ofst\=-.1))
    d += elm.Line().up(d.unit/4).at(Q12.emitter).dot()
    d += elm.Line().tox(Q9.emitter).dot()
    d += elm.Line().right(d.unit/4).at(Q12.base).dot()
    d += elm.Wire('|-').to(Q12.collector).dot().hold()
    d += elm.Line().right(d.unit\*1.5)
    d += (Q13 := elm.BjtPnp().anchor('base').label('Q13'))
    d += elm.Line().up(d.unit/4).dot()
    d += elm.Line().tox(Q12.emitter)
    d += (K := elm.Line().down(d.unit/5).at(Q13.collector).dot())
    d += elm.Line().down()
    d += (Q16 := elm.BjtNpn().right().anchor('collector').label('Q16', ofst\=-.1))
    d += elm.Line().left(d.unit/3).at(Q16.base).dot()
    d += (R7 := elm.Resistor().up().toy(K.end).label('R7\\n4.5K').dot())
    d += elm.Line().tox(Q13.collector).hold()
    d += (R8 := elm.Resistor().down().at(R7.start).label('R8\\n7.5K').dot())
    d += elm.Line().tox(Q16.emitter)
    d += (J := elm.Dot())
    d += elm.Line().toy(Q16.emitter)
    d += (Q15 := elm.BjtNpn().right().at(R8.end).anchor('collector').label('Q15'))
    d += elm.Line().left(d.unit/2).at(Q15.base).dot()
    d += (C1 := elm.Capacitor().toy(R7.end).label('C1\\n30pF'))
    d += elm.Line().tox(Q13.collector)
    d += elm.Line().at(C1.start).tox(Q6.collector).dot()
    d += elm.Line().down(d.unit/2).at(J.center)
    d += (Q19 := elm.BjtNpn().right().anchor('collector').label('Q19'))
    d += elm.Line().at(Q19.base).tox(Q15.emitter).dot()
    d += elm.Line().toy(Q15.emitter).hold()
    d += elm.Line().down(d.unit/4).at(Q19.emitter).dot()
    d += elm.Line().left()
    d += (Q22 := elm.BjtNpn().left().anchor('base').flip().label('Q22', 'left'))
    d += elm.Line().at(Q22.collector).toy(Q15.base).dot()
    d += elm.Line().at(Q22.emitter).toy(R3.start).dot()
    d += elm.Line().tox(R3.start).hold()
    d += elm.Line().tox(Q15.emitter).dot()
    d.push()
    d += elm.Resistor().up().label('R12\\n50K')
    d += elm.Line().toy(Q19.base)
    d.pop()
    d += elm.Line().tox(Q19.emitter).dot()
    d += (R11 := elm.Resistor().up().label('R11\\n50'))
    d += elm.Line().toy(Q19.emitter)

    d += elm.Line().up(d.unit/4).at(Q13.emitter)
    d += elm.Line().right(d.unit\*1.5).dot()
    d += elm.Line().length(d.unit/4).label('V+', 'right').hold()
    d += elm.Line().down(d.unit\*.75)
    d += (Q14 := elm.BjtNpn().right().anchor('collector').label('Q14'))
    d += elm.Line().left(d.unit/2).at(Q14.base)
    d.push()
    d += elm.Line().down(d.unit/2).idot()
    d += (Q17 := elm.BjtNpn().left().anchor('collector').flip().label('Q17', 'left', ofst\=-.1))
    d += elm.Line().at(Q17.base).tox(Q14.emitter).dot()
    d += (J := elm.Line().toy(Q14.emitter))
    d.pop()
    d += elm.Line().tox(Q13.collector).dot()
    d += elm.Resistor().down().at(J.start).label('R9\\n25').dot()
    d += elm.Wire('-|').to(Q17.emitter).hold()
    d += elm.Line().down(d.unit/4).dot()
    d += elm.Line().right(d.unit/4).label('OUT', 'right').hold()
    d += elm.Resistor().down().label('R10\\n50')
    d += (Q20 := elm.BjtPnp().right().anchor('emitter').label('Q20'))
    d += elm.Wire('c', k\=-1).at(Q20.base).to(Q15.collector)
    d += elm.Line().at(Q20.collector).toy(R3.start).dot()
    d += elm.Line().right(d.unit/4).label('V-', 'right').hold()
    d += elm.Line().tox(R11.start)

### Integrated Circuits[¶](#integrated-circuits "Link to this heading")

#### 555 LED Blinker Circuit[¶](#led-blinker-circuit "Link to this heading")

Using the [`schemdraw.elements.intcircuits.Ic`](index.html#schemdraw.elements.intcircuits.Ic "schemdraw.elements.intcircuits.Ic") class to define a custom integrated circuit.

![_images/ic_1_0.svg](_images/ic_1_0.svg)

with schemdraw.Drawing() as d:
    d.config(fontsize\=12)
    IC555def \= elm.Ic(pins\=\[elm.IcPin(name\='TRG', side\='left', pin\='2'),
                            elm.IcPin(name\='THR', side\='left', pin\='6'),
                            elm.IcPin(name\='DIS', side\='left', pin\='7'),
                            elm.IcPin(name\='CTL', side\='right', pin\='5'),
                            elm.IcPin(name\='OUT', side\='right', pin\='3'),
                            elm.IcPin(name\='RST', side\='top', pin\='4'),
                            elm.IcPin(name\='Vcc', side\='top', pin\='8'),
                            elm.IcPin(name\='GND', side\='bot', pin\='1'),\],
                       edgepadW\=.5,
                       edgepadH\=1,
                       pinspacing\=1.5,
                       leadlen\=1,
                       label\='555')
    d += (T := IC555def)
    d += (BOT := elm.Ground().at(T.GND))
    d += elm.Dot()
    d += elm.Resistor().endpoints(T.DIS, T.THR).label('Rb').idot()
    d += elm.Resistor().up().at(T.DIS).label('Ra').label('+Vcc', 'right')
    d += elm.Line().endpoints(T.THR, T.TRG)
    d += elm.Capacitor().at(T.TRG).toy(BOT.start).label('C')
    d += elm.Line().tox(BOT.start)
    d += elm.Capacitor().at(T.CTL).toy(BOT.start).label('.01$\\mu$F', 'bottom').dot()
    d += elm.Dot().at(T.DIS)
    d += elm.Dot().at(T.THR)
    d += elm.Dot().at(T.TRG)
    d += elm.Line().endpoints(T.RST,T.Vcc).dot()
    d += elm.Line().up(d.unit/4).label('+Vcc', 'right')
    d += elm.Resistor().right().at(T.OUT).label('330')
    d += elm.LED().flip().toy(BOT.start)
    d += elm.Line().tox(BOT.start)

#### Seven-Segment Display Counter[¶](#seven-segment-display-counter "Link to this heading")

![_images/ic_2_0.svg](_images/ic_2_0.svg)

with schemdraw.Drawing() as d:
    d.config(fontsize\=12)
    d += (IC555 := elm.Ic555())
    d += (gnd := elm.Ground(xy\=IC555.GND))
    d += elm.Dot()
    d += elm.Resistor().endpoints(IC555.DIS, IC555.THR).label('100 kΩ')
    d += elm.Resistor().up().at(IC555.DIS).label('1 kΩ').label('+Vcc', 'right')
    d += elm.Line().endpoints(IC555.THR, IC555.TRG)
    d += elm.Capacitor(polar\=True).at(IC555.TRG).toy(gnd.start).label('10 μF')
    d += elm.Line().tox(gnd.start)
    d += elm.Capacitor().at(IC555.CTL).toy(gnd.start).label('.01 μF', 'bottom')
    d += elm.Line().tox(gnd.start)

    d += elm.Dot().at(IC555.DIS)
    d += elm.Dot().at(IC555.THR)
    d += elm.Dot().at(IC555.TRG)
    d += elm.Line().endpoints(IC555.RST,IC555.Vcc).dot()
    d += elm.Line().up(d.unit/4).label('+Vcc', 'right')

    IC4026 \= elm.Ic(pins\=\[elm.IcPin('CLK', pin\='1', side\='left'),
                          elm.IcPin('INH', pin\='2', side\='left'), \# Inhibit
                          elm.IcPin('RST', pin\='15', side\='left'),
                          elm.IcPin('DEI', pin\='3', side\='left'), \# Display Enable In
                          elm.IcPin('Vss', pin\='8', side\='bot'),
                          elm.IcPin('Vdd', pin\='16', side\='top'),
                          elm.IcPin('UCS', pin\='14', side\='bot'), \# Ungated C Segment
                          elm.IcPin('DEO', pin\='4', side\='bot'),  \# Display Enable Out
                          elm.IcPin('Co', pin\='4', side\='bot'),   \# Carry out
                          elm.IcPin('g', pin\='7', side\='right'),
                          elm.IcPin('f', pin\='6', side\='right'),
                          elm.IcPin('e', pin\='11', side\='right'),
                          elm.IcPin('d', pin\='9', side\='right'),
                          elm.IcPin('c', pin\='13', side\='right'),
                          elm.IcPin('b', pin\='12', side\='right'),
                          elm.IcPin('a', pin\='10', side\='right'),
                         \],
                   w\=4, leadlen\=.8).label('4026').right()

    d.move\_from(IC555.OUT, dx\=5, dy\=-1)
    d += IC4026.anchor('center')
    d += elm.Wire('c').at(IC555.OUT).to(IC4026.CLK)
    d += elm.Line().endpoints(IC4026.INH, IC4026.RST).dot()
    d += elm.Line().left(d.unit/4)
    d += elm.Ground()
    d += elm.Wire('|-').at(IC4026.DEI).to(IC4026.Vdd).dot()
    d += elm.Line().up(d.unit/4).label('+Vcc', 'right')
    d += elm.Line().at(IC4026.Vss).tox(IC4026.UCS).dot()
    d += elm.Ground()
    d += elm.Line().tox(IC4026.DEO).dot()
    d += elm.Line().tox(IC4026.Co)

    d += elm.Resistor().right().at(IC4026.a)
    d += (disp := elm.SevenSegment(cathode\=True).anchor('a'))
    d += elm.Resistor().at(IC4026.b)
    d += elm.Resistor().at(IC4026.c)
    d += elm.Resistor().at(IC4026.d)
    d += elm.Resistor().at(IC4026.e)
    d += elm.Resistor().at(IC4026.f)
    d += elm.Resistor().at(IC4026.g).label('7 x 330', loc\='bottom')
    d += elm.Ground(lead\=False).at(disp.cathode)

#### Arduino Board[¶](#arduino-board "Link to this heading")

The Arduino board uses [`schemdraw.elements.connectors.OrthoLines`](index.html#schemdraw.elements.connectors.OrthoLines "schemdraw.elements.connectors.OrthoLines") to easily add all connections between data bus and headers.

![_images/ic_3_0.svg](_images/ic_3_0.svg)

class Atmega328(elm.Ic):
    def \_\_init\_\_(self, \*args, \*\*kwargs):
        pins\=\[elm.IcPin(name\='PD0', pin\='2', side\='r', slot\='1/22'),
              elm.IcPin(name\='PD1', pin\='3', side\='r', slot\='2/22'),
              elm.IcPin(name\='PD2', pin\='4', side\='r', slot\='3/22'),
              elm.IcPin(name\='PD3', pin\='5', side\='r', slot\='4/22'),
              elm.IcPin(name\='PD4', pin\='6', side\='r', slot\='5/22'),
              elm.IcPin(name\='PD5', pin\='11', side\='r', slot\='6/22'),
              elm.IcPin(name\='PD6', pin\='12', side\='r', slot\='7/22'),
              elm.IcPin(name\='PD7', pin\='13', side\='r', slot\='8/22'),
              elm.IcPin(name\='PC0', pin\='23', side\='r', slot\='10/22'),
              elm.IcPin(name\='PC1', pin\='24', side\='r', slot\='11/22'),
              elm.IcPin(name\='PC2', pin\='25', side\='r', slot\='12/22'),
              elm.IcPin(name\='PC3', pin\='26', side\='r', slot\='13/22'),
              elm.IcPin(name\='PC4', pin\='27', side\='r', slot\='14/22'),
              elm.IcPin(name\='PC5', pin\='28', side\='r', slot\='15/22'),
              elm.IcPin(name\='PB0', pin\='14', side\='r', slot\='17/22'),
              elm.IcPin(name\='PB1', pin\='15', side\='r', slot\='18/22'),
              elm.IcPin(name\='PB2', pin\='16', side\='r', slot\='19/22'),
              elm.IcPin(name\='PB3', pin\='17', side\='r', slot\='20/22'),
              elm.IcPin(name\='PB4', pin\='18', side\='r', slot\='21/22'),
              elm.IcPin(name\='PB5', pin\='19', side\='r', slot\='22/22'),

              elm.IcPin(name\='RESET', side\='l', slot\='22/22', invert\=True, pin\='1'),
              elm.IcPin(name\='XTAL2', side\='l', slot\='19/22', pin\='10'),
              elm.IcPin(name\='XTAL1', side\='l', slot\='17/22', pin\='9'),
              elm.IcPin(name\='AREF', side\='l', slot\='15/22', pin\='21'),
              elm.IcPin(name\='AVCC', side\='l', slot\='14/22', pin\='20'),
              elm.IcPin(name\='AGND', side\='l', slot\='13/22', pin\='22'),
              elm.IcPin(name\='VCC', side\='l', slot\='11/22', pin\='7'),
              elm.IcPin(name\='GND', side\='l', slot\='10/22', pin\='8')\]
        super().\_\_init\_\_(pins\=pins, w\=5, plblofst\=.05, botlabel\='ATMEGA328', \*\*kwargs)

with schemdraw.Drawing() as d:
    d.config(fontsize\=11, inches\_per\_unit\=.4)
    d += (Q1 := Atmega328())
    d += (JP4 := elm.Header(rows\=10, shownumber\=True, pinsright\=\['D8', 'D9', 'D10', 'D11', 'D12', 'D13', '', '', '', ''\], pinalignright\='center')
                            .flip().at(Q1.PB5, dx\=4, dy\=1).anchor('pin6').label('JP4', fontsize\=10))

    d += (JP3 := elm.Header(rows\=6, shownumber\=True, pinsright\=\['A0', 'A1', 'A2', 'A3', 'A4', 'A5'\], pinalignright\='center')
                        .flip().at(Q1.PC5, dx\=4).anchor('pin6').label('JP3', fontsize\=10))

    d += (JP2 := elm.Header(rows\=8, shownumber\=True, pinsright\=\['D0', 'D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7'\],
                            pinalignright\='center')).at(Q1.PD7, dx\=3).flip().anchor('pin8').label('JP2', fontsize\=10)

    d += elm.OrthoLines(n\=6).at(Q1.PB5).to(JP4.pin6)
    d += elm.OrthoLines(n\=6).at(Q1.PC5).to(JP3.pin6)
    d += elm.OrthoLines(n\=8).at(Q1.PD7).to(JP2.pin8)

    d += elm.Line().left(.9).at(JP4.pin7).label('GND', 'left')
    d += elm.Line().left(.9).at(JP4.pin8).label('AREF', 'left')
    d += elm.Line().left(.9).at(JP4.pin9).label('AD4/SDA', 'left')
    d += elm.Line().left(.9).at(JP4.pin10).label('AD5/SCL', 'left')

    d += (JP1 := elm.Header(rows\=6, shownumber\=True, pinsright\=\['VCC', 'RXD', 'TXD', 'DTR', 'RTS', 'GND'\],
                            pinalignright\='center').right().at(Q1.PD0, dx\=4, dy\=-2).anchor('pin1'))
    d += elm.Line().left(d.unit/2).at(JP1.pin1)
    d += elm.Vdd().label('+5V')
    d += elm.Line().left().at(JP1.pin2)
    d += elm.Line().toy(Q1.PD0).dot()
    d += elm.Line().left(d.unit+.6).at(JP1.pin3)
    d += elm.Line().toy(Q1.PD1).dot()
    d += elm.Line().left(d.unit/2).at(JP1.pin6)
    d += elm.Ground()

    d += elm.Line().left(d.unit\*2).at(Q1.XTAL2).dot()
    d.push()
    d += elm.Capacitor().left(d.unit/2).scale(.75)
    d += elm.Line().toy(Q1.XTAL1).dot()
    d += elm.Ground()
    d += elm.Capacitor().right(d.unit/2).scale(.75).dot()
    d.pop()
    d += elm.Crystal().toy(Q1.XTAL1).label('16MHz', 'bottom')
    d += elm.Line().tox(Q1.XTAL1)

    d += elm.Line().left(d.unit/3).at(Q1.AREF).label('AREF', 'left')
    d += elm.Line().left(1.5\*d.unit).at(Q1.AVCC)
    d += elm.Vdd().label('+5V')
    d += elm.Line().toy(Q1.VCC).dot().idot()
    d += elm.Line().tox(Q1.VCC).hold()
    d += elm.Capacitor().down().label('100n')
    d += (GND := elm.Ground())

    d += elm.Line().left().at(Q1.AGND)
    d += elm.Line().toy(Q1.GND).dot()
    d += elm.Line().tox(Q1.GND).hold()
    d += elm.Wire('|-').to(GND.center).dot()

    d += elm.Line().left().at(Q1.RESET).dot()
    d.push()
    d += elm.RBox().up().label('10K')
    d += elm.Vdd().label('+5V')
    d.pop()
    d += elm.Line().left().dot()
    d.push()
    d += (RST := elm.Button().up().label('Reset'))
    d += elm.Line().left(d.unit/2)
    d += elm.Ground()
    d.pop()

    d += elm.Capacitor().left().at(JP1.pin4).label('100n', 'bottom')
    d += elm.Wire('c', k\=-16).to(RST.start)

#### 741 Opamp, DIP Layout[¶](#opamp-dip-layout "Link to this heading")

![_images/ic_4_0.svg](_images/ic_4_0.svg)

with schemdraw.Drawing() as d:
    d += (Q := elm.IcDIP(pins\=8)
                 .label('Offset Null', loc\='p1', fontsize\=10)
                 .label('Inverting Input', loc\='p2', fontsize\=10)
                 .label('Non-inverting Input', loc\='p3', fontsize\=10)
                 .label('V-', loc\='p4', fontsize\=10)
                 .label('Offset Null', loc\='p5', fontsize\=10)
                 .label('Output', loc\='p6', fontsize\=10)
                 .label('V+', loc\='p7', fontsize\=10)
                 .label('NC', loc\='p8', fontsize\=10))
    d += elm.Line().at(Q.p2\_in).length(d.unit/5)
    d += (op := elm.Opamp().anchor('in1').scale(.8))
    d += elm.Line().at(Q.p3\_in).length(d.unit/5)
    d += elm.Wire('c', k\=.3).at(op.out).to(Q.p6\_in)
    d += elm.Wire('-|').at(Q.p4\_in).to(op.n1)
    d += elm.Wire('-|').at(Q.p7\_in).to(op.n2)

### Signal Processing[¶](#signal-processing "Link to this heading")

Signal processing elements are in the [`schemdraw.dsp.dsp`](index.html#module-schemdraw.dsp.dsp "schemdraw.dsp.dsp") module.

from schemdraw import dsp

#### Various Networks[¶](#various-networks "Link to this heading")

![_images/signalproc_1_0.svg](_images/signalproc_1_0.svg)

with schemdraw.Drawing() as d:
    d += dsp.Line().length(d.unit/3).label('in')
    d += (inpt := dsp.Dot())
    d += dsp.Arrow().length(d.unit/3)
    d += (delay := dsp.Box(w\=2, h\=2).anchor('W').label('Delay\\nT'))
    d += dsp.Arrow().right(d.unit/2).at(delay.E)
    d += (sm := dsp.SumSigma())
    d += dsp.Arrow().at(sm.E).length(d.unit/2)
    d += (intg := dsp.Box(w\=2, h\=2).anchor('W').label('$\\int$'))
    d += dsp.Arrow().right(d.unit/2).at(intg.E).label('out', loc\='right')
    d += dsp.Line().down(d.unit/2).at(inpt.center)
    d += dsp.Line().tox(sm.S)
    d += dsp.Arrow().toy(sm.S).label('+', loc\='bot')

![_images/signalproc_2_0.svg](_images/signalproc_2_0.svg)

with schemdraw.Drawing() as d:
    d.config(fontsize\=14)
    d += dsp.Line().length(d.unit/2).label('F(s)').dot()
    d.push()
    d += dsp.Line().up(d.unit/2)
    d += dsp.Arrow().right(d.unit/2)
    d += (h1 := dsp.Box(w\=2, h\=2).anchor('W').label('$H\_1(s)$'))
    d.pop()
    d += dsp.Line().down(d.unit/2)
    d += dsp.Arrow().right(d.unit/2)
    d += (h2 := dsp.Box(w\=2, h\=2).anchor('W').label('$H\_2(s)$'))
    d += (sm := dsp.SumSigma().right().at((h1.E\[0\] + d.unit/2, 0)).anchor('center'))
    d += dsp.Line().at(h1.E).tox(sm.N)
    d += dsp.Arrow().toy(sm.N)
    d += dsp.Line().at(h2.E).tox(sm.S)
    d += dsp.Arrow().toy(sm.S)
    d += dsp.Arrow().right(d.unit/3).at(sm.E).label('Y(s)', 'right')

#### Superheterodyne Receiver[¶](#superheterodyne-receiver "Link to this heading")

[Source](https://www.electronicdesign.com/adc/high-speed-rf-sampling-adc-boosts-bandwidth-dynamic-range).

![_images/signalproc_3_0.svg](_images/signalproc_3_0.svg)

with schemdraw.Drawing() as d:
    d.config(fontsize\=12)
    d += dsp.Antenna()
    d += dsp.Line().right(d.unit/4)
    d += dsp.Filter(response\='bp').fill('thistle').anchor('W').label('RF filter\\n#1', 'bottom', ofst\=.2)
    d += dsp.Line().length(d.unit/4)
    d += dsp.Amp().fill('lightblue').label('LNA')
    d += dsp.Line().length(d.unit/4)
    d += dsp.Filter(response\='bp').anchor('W').fill('thistle').label('RF filter\\n#2', 'bottom', ofst\=.2)
    d += dsp.Line().length(d.unit/3)
    d += (mix := dsp.Mixer().fill('navajowhite').label('Mixer'))
    d += dsp.Line().at(mix.S).down(d.unit/3)
    d += dsp.Oscillator().right().anchor('N').fill('navajowhite').label('Local\\nOscillator', 'right', ofst\=.2)
    d += dsp.Line().at(mix.E).right(d.unit/3)
    d += dsp.Filter(response\='bp').anchor('W').fill('thistle').label('IF filter', 'bottom', ofst\=.2)
    d += dsp.Line().right(d.unit/4)
    d += dsp.Amp().fill('lightblue').label('IF\\namplifier')
    d += dsp.Line().length(d.unit/4)
    d += dsp.Demod().anchor('W').fill('navajowhite').label('Demodulator', 'bottom', ofst\=.2)
    d += dsp.Arrow().right(d.unit/3)

#### Direct Conversion Receiver[¶](#direct-conversion-receiver "Link to this heading")

![_images/signalproc_4_0.svg](_images/signalproc_4_0.svg)

with schemdraw.Drawing() as d:
    d += dsp.Antenna()
    d += dsp.Arrow().right(d.unit/2).label('$f\_{RF}$', 'bot')
    d += dsp.Amp().label('LNA')
    d += dsp.Line().right(d.unit/5).dot()
    d.push()
    d += dsp.Line().length(d.unit/4)
    d += (mix1 := dsp.Mixer().label('Mixer', ofst\=0))
    d += dsp.Arrow().length(d.unit/2)
    d += (lpf1 := dsp.Filter(response\='lp').label('LPF', 'bot', ofst\=.2))
    d += dsp.Line().length(d.unit/6)
    d += (adc1 := dsp.Adc().label('ADC'))
    d += dsp.Arrow().length(d.unit/3)
    d += (dsp1 := dsp.Ic(pins\=\[dsp.IcPin(side\='L'), dsp.IcPin(side\='L'), dsp.IcPin(side\='R')\],
                        size\=(2.75, 5), leadlen\=0).anchor('inL2').label('DSP'))
    d += dsp.Arrow().at(dsp1.inR1).length(d.unit/3)
    d.pop()

    d += dsp.Line().toy(dsp1.inL1)
    d += dsp.Arrow().tox(mix1.W)
    d += (mix2 := dsp.Mixer().label('Mixer', ofst\=0))
    d += dsp.Arrow().tox(lpf1.W)
    d += dsp.Filter(response\='lp').label('LPF', 'bot', ofst\=.2)
    d += dsp.Line().tox(adc1.W)
    d += dsp.Adc().label('ADC')
    d += dsp.Arrow().to(dsp1.inL1)

    d += dsp.Arrow().down(d.unit/6).reverse().at(mix1.S)
    d += dsp.Line().left(d.unit\*1.25)
    d += dsp.Line().down(d.unit\*.75)
    d += (flo := dsp.Dot().label('$f\_{LO}$', 'left'))
    d.push()
    d += dsp.Line().down(d.unit/5)
    d += dsp.Oscillator().right().anchor('N').label('LO', 'left', ofst\=.15)
    d.pop()
    d += dsp.Arrow().down(d.unit/4).reverse().at(mix2.S)
    d += (b1 := dsp.Square().right().label('90°').anchor('N'))
    d += dsp.Arrow().left(d.unit/4).reverse().at(b1.W)
    d += dsp.Line().toy(flo.center)
    d += dsp.Line().tox(flo.center)

#### Digital Filter[¶](#digital-filter "Link to this heading")

![_images/signalproc_5_0.svg](_images/signalproc_5_0.svg)

with schemdraw.Drawing() as d:
    d.config(unit\=1, fontsize\=14)
    d += dsp.Line().length(d.unit\*2).label('x\[n\]', 'left').dot()

    d.push()
    d += dsp.Line().right()
    d += dsp.Amp().label('$b\_0$', 'bottom')
    d += dsp.Arrow()
    d += (s0 := dsp.Sum().anchor('W'))
    d.pop()

    d += dsp.Arrow().down()
    d += (z1 := dsp.Square(label\='$z^{-1}$'))
    d += dsp.Line().length(d.unit/2).dot()

    d.push()
    d += dsp.Line().right()
    d += dsp.Amp().label('$b\_1$', 'bottom')
    d += dsp.Arrow()
    d += (s1 := dsp.Sum().anchor('W'))
    d.pop()

    d += dsp.Arrow().down(d.unit\*.75)
    d += dsp.Square().label('$z^{-1}$')
    d += dsp.Line().length(d.unit\*.75)
    d += dsp.Line().right()
    d += dsp.Amp().label('$b\_2$', 'bottom')
    d += dsp.Arrow()
    d += (s2 := dsp.Sum().anchor('W'))

    d += dsp.Arrow().at(s2.N).toy(s1.S)
    d += dsp.Arrow().at(s1.N).toy(s0.S)

    d += dsp.Line().right(d.unit\*2.75).at(s0.E).dot()
    d += dsp.Arrow().right().label('y\[n\]', 'right').hold()
    d += dsp.Arrow().down()
    d += dsp.Square().label('$z^{-1}$')
    d += dsp.Line().length(d.unit/2).dot()
    d.push()
    d += dsp.Line().left()
    d += (a1 := dsp.Amp().label('$-a\_1$', 'bottom'))
    d += dsp.Arrow().at(a1.out).tox(s1.E)
    d.pop()

    d += dsp.Arrow().down(d.unit\*.75)
    d += dsp.Square().label('$z^{-1}$')
    d += dsp.Line().length(d.unit\*.75)
    d += dsp.Line().left()
    d += (a2 := dsp.Amp().label('$-a\_2$', 'bottom'))
    d += dsp.Arrow().at(a2.out).tox(s2.E)

### Flowcharting[¶](#flowcharting "Link to this heading")

Flowchart elements are defined in the `flow` module.

from schemdraw import flow

#### It’s a Trap![¶](#it-s-a-trap "Link to this heading")

Recreation of [XKCD 1195](https://xkcd.com/1195/).

![_images/flowcharting_1_0.svg](_images/flowcharting_1_0.svg)

with schemdraw.Drawing() as d:
    d += flow.Start().label('START')
    d += flow.Arrow().down(d.unit/3)
    d += (h := flow.Decision(w\=5.5, h\=4, S\='YES').label('Hey, wait,\\nthis flowchart\\nis a trap!'))
    d += flow.Line().down(d.unit/4)
    d += flow.Wire('c', k\=3.5, arrow\='->').to(h.E)

#### Flowchart for flowcharts[¶](#flowchart-for-flowcharts "Link to this heading")

Recreation of [XKCD 518](https://xkcd.com/518/).

![_images/flowcharting_2_0.svg](_images/flowcharting_2_0.svg)

with schemdraw.Drawing() as d:
    d.config(fontsize\=11)
    d += (b := flow.Start().label('START'))
    d += flow.Arrow().down(d.unit/2)
    d += (d1 := flow.Decision(w\=5, h\=3.9, E\='YES', S\='NO').label('DO YOU\\nUNDERSTAND\\nFLOW CHARTS?'))
    d += flow.Arrow().length(d.unit/2)
    d += (d2 := flow.Decision(w\=5, h\=3.9, E\='YES', S\='NO').label('OKAY,\\nYOU SEE THE\\nLINE LABELED\\n"YES"?'))
    d += flow.Arrow().length(d.unit/2)
    d += (d3 := flow.Decision(w\=5.2, h\=3.9, E\='YES', S\='NO').label('BUT YOU\\nSEE THE ONES\\nLABELED "NO".'))

    d += flow.Arrow().right(d.unit/2).at(d3.E)
    d += flow.Box(w\=2, h\=1.25).anchor('W').label('WAIT,\\nWHAT?')
    d += flow.Arrow().down(d.unit/2).at(d3.S)
    d += (listen := flow.Box(w\=2, h\=1).label('LISTEN.'))
    d += flow.Arrow().right(d.unit/2).at(listen.E)
    d += (hate := flow.Box(w\=2, h\=1.25).anchor('W').label('I HATE\\nYOU.'))

    d += flow.Arrow().right(d.unit\*3.5).at(d1.E)
    d += (good := flow.Box(w\=2, h\=1).anchor('W').label('GOOD'))
    d += flow.Arrow().right(d.unit\*1.5).at(d2.E)
    d += (d4 := flow.Decision(w\=5.3, h\=4.0, E\='YES', S\='NO').anchor('W').label('...AND YOU CAN\\nSEE THE ONES\\nLABELED "NO"?'))

    d += flow.Wire('-|', arrow\='->').at(d4.E).to(good.S)
    d += flow.Arrow().down(d.unit/2).at(d4.S)
    d += (d5 := flow.Decision(w\=5, h\=3.6, E\='YES', S\='NO').label('BUT YOU\\nJUST FOLLOWED\\nTHEM TWICE!'))
    d += flow.Arrow().right().at(d5.E)
    d += (question := flow.Box(w\=3.5, h\=1.75).anchor('W').label("(THAT WASN'T\\nA QUESTION.)"))
    d += flow.Wire('n', k\=-1, arrow\='->').at(d5.S).to(question.S)

    d += flow.Line().at(good.E).tox(question.S)
    d += flow.Arrow().down()
    d += (drink := flow.Box(w\=2.5, h\=1.5).label("LET'S GO\\nDRINK."))
    d += flow.Arrow().right().at(drink.E).label('6 DRINKS')
    d += flow.Box(w\=3.7, h\=2).anchor('W').label('HEY, I SHOULD\\nTRY INSTALLING\\nFREEBSD!')
    d += flow.Arrow().up(d.unit\*.75).at(question.N)
    d += (screw := flow.Box(w\=2.5, h\=1).anchor('S').label('SCREW IT.'))
    d += flow.Arrow().at(screw.N).toy(drink.S)

#### State Machine Acceptor[¶](#state-machine-acceptor "Link to this heading")

[Source](https://en.wikipedia.org/wiki/Finite-state_machine#/media/File:DFAexample.svg)

![_images/flowcharting_3_0.svg](_images/flowcharting_3_0.svg)

with schemdraw.Drawing() as d:
    d += elm.Arrow().length(1)
    d += (s1 := flow.StateEnd().anchor('W').label('$S\_1$'))
    d += elm.Arc2(arrow\='<-').at(s1.NE).label('0')
    d += (s2 := flow.State().anchor('NW').label('$S\_2$'))
    d += elm.Arc2(arrow\='<-').at(s2.SW).to(s1.SE).label('0')
    d += elm.ArcLoop(arrow\='<-').at(s2.NE).to(s2.E).label('1')
    d += elm.ArcLoop(arrow\='<-').at(s1.NW).to(s1.N).label('1')

#### Door Controller[¶](#door-controller "Link to this heading")

[Diagram Source](https://en.wikipedia.org/wiki/Finite-state_machine#/media/File:Fsm_Moore_model_door_control.svg)

![_images/flowcharting_4_0.svg](_images/flowcharting_4_0.svg)

with schemdraw.Drawing() as d:
    d.config(fontsize\=12)
    delta \= 4
    d += (c4 := flow.Circle(r\=1).label('4\\nopening'))
    d += (c1 := flow.Circle(r\=1).at((delta, delta)).label('1\\nopened'))
    d += (c2 := flow.Circle(r\=1).at((2\*delta, 0)).label('2\\nclosing'))
    d += (c3 := flow.Circle(r\=1).at((delta, \-delta)).label('3\\nclosed'))
    d += elm.Arc2(arrow\='->', k\=.3).at(c4.NNE).to(c1.WSW).label('sensor\\nopened')
    d += elm.Arc2(arrow\='->', k\=.3).at(c1.ESE).to(c2.NNW).label('close')
    d += elm.Arc2(arrow\='->', k\=.3).at(c2.SSW).to(c3.ENE).label('sensor\\nclosed')
    d += elm.Arc2(arrow\='->', k\=.3).at(c3.WNW).to(c4.SSE).label('open')
    d += elm.Arc2(arrow\='<-', k\=.3).at(c4.ENE).to(c2.WNW).label('open')
    d += elm.Arc2(arrow\='<-', k\=.3).at(c2.WSW).to(c4.ESE).label('close')

#### Another State Machine[¶](#another-state-machine "Link to this heading")

![_images/flowcharting_5_0.svg](_images/flowcharting_5_0.svg)

with schemdraw.Drawing() as dwg:
    dwg += (a := flow.Circle().label('a').fill('lightblue'))
    dwg += (b := flow.Circle().at((4, 0)).label('b').fill('lightblue'))
    dwg += (c := flow.Circle().at((8, 0)).label('c').fill('lightblue'))
    dwg += (f := flow.Circle().at((0, \-4)).label('f').fill('lightblue'))
    dwg += (e := flow.Circle().at((4, \-6)).label('e').fill('lightblue'))
    dwg += (d := flow.Circle().at((8, \-4)).label('d').fill('lightblue'))
    dwg += elm.ArcLoop(arrow\='->').at(a.NW).to(a.NNE).label('00/0', fontsize\=10)
    dwg += elm.ArcLoop(arrow\='->').at(b.NNW).to(b.NE).label('01/0', fontsize\=10)
    dwg += elm.ArcLoop(arrow\='->').at(c.NNW).to(c.NE).label('11/0', fontsize\=10)
    dwg += elm.ArcLoop(arrow\='->').at(d.E).to(d.SE).label('10/0', fontsize\=10)
    dwg += elm.ArcLoop(arrow\='->').at(e.SSE).to(e.SW).label('11/1', fontsize\=10)
    dwg += elm.ArcLoop(arrow\='->').at(f.S).to(f.SW).label('01/1', fontsize\=10)
    dwg += elm.Arc2(k\=.1, arrow\='<-').at(a.ENE).to(b.WNW).label('01/0', fontsize\=10)
    dwg += elm.Arc2(k\=.1, arrow\='<-').at(b.W).to(a.E).label('00/0', fontsize\=10)
    dwg += elm.Arc2(k\=.1, arrow\='<-').at(b.ENE).to(c.WNW).label('11/0', fontsize\=10)
    dwg += elm.Arc2(k\=.1, arrow\='<-').at(c.W).to(b.E).label('01/0', fontsize\=10)
    dwg += elm.Arc2(k\=.1, arrow\='<-').at(a.ESE).to(d.NW).label('00/0', fontsize\=10)
    dwg += elm.Arc2(k\=.1, arrow\='<-').at(d.WNW).to(a.SE).label('10/0', fontsize\=10)
    dwg += elm.Arc2(k\=.1, arrow\='<-').at(f.ENE).to(e.NW).label('01/1', fontsize\=10)
    dwg += elm.Arc2(k\=.1, arrow\='<-').at(e.WNW).to(f.ESE).label('11/1', fontsize\=10)
    dwg += elm.Arc2(k\=.1, arrow\='->').at(e.NE).to(d.WSW).label('11/1', fontsize\=10)
    dwg += elm.Arc2(k\=.1, arrow\='->').at(d.SSW).to(e.ENE).label('10/0', fontsize\=10)
    dwg += elm.Arc2(k\=.1, arrow\='<-').at(f.NNW).to(a.SSW).label('00/0', fontsize\=10)
    dwg += elm.Arc2(k\=.1, arrow\='<-').at(c.SSE).to(d.NNE).label('10/0', fontsize\=10)

#### Logical Flow Diagram[¶](#logical-flow-diagram "Link to this heading")

![_images/flowcharting_6_0.svg](_images/flowcharting_6_0.svg)

with schemdraw.Drawing(unit\=1) as dwg:
    dwg += (a := flow.Circle(r\=.5).label('a'))
    dwg += (x := flow.Decision(w\=1.5, h\=1.5).label('$X$').at(a.S).anchor('N'))
    dwg += elm.RightLines(arrow\='->').at(x.E).label('$\\overline{X}$')
    dwg += (y1 := flow.Decision(w\=1.5, h\=1.5).label('$Y$'))
    dwg.move\_from(y1.N, dx\=-5)
    dwg += (y2 := flow.Decision(w\=1.5, h\=1.5).label('$Y$'))
    dwg += elm.RightLines(arrow\='->').at(x.W).to(y2.N).label('$X$')
    dwg += elm.Arrow().at(y2.S).label('$Y$')
    dwg += (b := flow.Circle(r\=.5).label('b'))
    dwg.move\_from(b.N, dx\=2)
    dwg += (c := flow.Circle(r\=.5).label('c'))
    dwg += elm.RightLines(arrow\='->').at(y2.E).to(c.N).label('$\\overline{Y}$')
    dwg += elm.Arrow().at(y1.S).label('$Y$')
    dwg += (d := flow.Circle(r\=.5).label('d'))
    dwg.move\_from(d.N, dx\=2)
    dwg += (e := flow.Circle(r\=.5).label('e'))
    dwg += elm.RightLines(arrow\='->').at(y1.E).to(e.N).label('$\\overline{Y}$')

### Styles[¶](#styles "Link to this heading")

Circuit elements can be styled using Matplotlib colors, line-styles, and line widths.

#### Resistor circle[¶](#resistor-circle "Link to this heading")

Uses named colors in a loop.

![_images/styles_1_0.svg](_images/styles_1_0.svg)

with schemdraw.Drawing() as d:
    for i, color in enumerate(\['red', 'orange', 'yellow', 'yellowgreen', 'green', 'blue', 'indigo', 'violet'\]):
        d += elm.Resistor().theta(45\*i+20).color(color).label('R{}'.format(i))

#### Hand-drawn[¶](#hand-drawn "Link to this heading")

And for a change of pace, activate Matplotlib’s XKCD mode for “hand-drawn” look!

![_images/styles_2_0.svg](_images/styles_2_0.svg)

import matplotlib.pyplot as plt
plt.xkcd()

with schemdraw.Drawing() as d:
    d += (op := elm.Opamp(leads\=True))
    d += elm.Line().down().at(op.in2).length(d.unit/4)
    d += elm.Ground(lead\=False)
    d += (Rin := elm.Resistor().at(op.in1).left().idot().label('$R\_{in}$', loc\='bot').label('$v\_{in}$', loc\='left'))
    d += elm.Line().up().at(op.in1).length(d.unit/2)
    d += elm.Resistor().tox(op.out).label('$R\_f$')
    d += elm.Line().toy(op.out).dot()
    d += elm.Line().right().at(op.out).length(d.unit/4).label('$v\_{o}$', loc\='right')

* * *

Need more circuit examples? Check out the Schemdraw Examples Pack on buymeacoffee.com:

[![Buy Me A Coffee](https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png)](https://www.buymeacoffee.com/cdelker/e/55648)

Customizing Elements[¶](#customizing-elements "Link to this heading")
---------------------------------------------------------------------

### Grouping Elements[¶](#grouping-elements "Link to this heading")

If a set of circuit elements are to be reused multiple times, they can be grouped into a single element. Create and populate a drawing, but set show=False. Instead, use the Drawing to create a new [`schemdraw.elements.ElementDrawing`](index.html#schemdraw.elements.ElementDrawing "schemdraw.elements.ElementDrawing"), which converts the drawing into an element instance to add to other drawings.

with schemdraw.Drawing(show\=False) as d1:
    d1 += elm.Resistor()
    d1.push()
    d1 += elm.Capacitor().down()
    d1 += elm.Line().left()
    d1.pop()

with schemdraw.Drawing() as d2:  \# Add a second drawing
    for i in range(3):        d2 += elm.ElementDrawing(d1)   \# Add the first drawing to it 3 times

![_images/customizing_1_0.svg](_images/customizing_1_0.svg)

### Defining custom elements[¶](#defining-custom-elements "Link to this heading")

All elements are subclasses of [`schemdraw.elements.Element`](index.html#schemdraw.elements.Element "schemdraw.elements.Element") or [`schemdraw.elements.Element2Term`](index.html#schemdraw.elements.Element2Term "schemdraw.elements.Element2Term"). For elements consisting of several other already-defined elements (like a relay), [`schemdraw.elements.compound.ElementCompound`](index.html#schemdraw.elements.compound.ElementCompound "schemdraw.elements.compound.ElementCompound") can be used for easy combining of multiple elements. Subclasses only need to define the \_\_init\_\_ method in order to add lines, shapes, and text to the new element, all of which are defined using [`schemdraw.segments.Segment`](index.html#schemdraw.segments.Segment "schemdraw.segments.Segment") classes. New Segments should be appended to the Element.segments attribute list.

Coordinates are all defined in element cooridnates, where the element begins at (0, 0) and is drawn from left to right. The drawing engine will rotate and translate the element to its final position, and for two-terminal elements deriving from Element2Term, will add lead extensions to the correct length depending on the element’s placement parameters. Therefore elements deriving from Element2Term should not define the lead extensions (e.g. a Resistor only defines the zig-zag portion). A standard resistor is 1 drawing unit long, and with default lead extension will become 3 units long.

Segments include [`schemdraw.segments.Segment`](index.html#schemdraw.segments.Segment "schemdraw.segments.Segment"), [`schemdraw.segments.SegmentPoly`](index.html#schemdraw.segments.SegmentPoly "schemdraw.segments.SegmentPoly"), [`schemdraw.segments.SegmentCircle`](index.html#schemdraw.segments.SegmentCircle "schemdraw.segments.SegmentCircle"), [`schemdraw.segments.SegmentArc`](index.html#schemdraw.segments.SegmentArc "schemdraw.segments.SegmentArc"), [`schemdraw.segments.SegmentText`](index.html#schemdraw.segments.SegmentText "schemdraw.segments.SegmentText"), and [`schemdraw.segments.SegmentBezier`](index.html#schemdraw.segments.SegmentBezier "schemdraw.segments.SegmentBezier").

The subclassed Element.\_\_init\_\_ method can be defined with extra parameters to help define the element options.

In addition to the list of Segments, any named anchors and other parameters should be specified. Anchors should be added to the Element.anchors dictionary as {name: (x, y)} key/value pairs.

The Element instance maintains its own parameters dictionary in Element.params that override the default drawing parameters. Parameters are resolved by a ChainMap of user arguments to the Element instance, the Element.params attribute, then the schemdraw.Drawing parameters, in that order. A common use of setting Element.params in the setup function is to change the default position of text labels, for example Transistor elements apply labels on the right side of the element by default, so they add to the setup:

self.params\['lblloc'\] \= 'rgt'

The user can still override this label position by creating, for example, Transistor().label(‘Q1’, loc=’top’).

As an example, here’s the definition of our favorite element, the resistor:

class Resistor(Element2Term):
    def \_\_init\_\_(self, \*d, \*\*kwargs):
        super().\_\_init\_\_(\*d, \*\*kwargs)
        self.segments.append(Segment(\[(0, 0),
                                      (0.5\*reswidth, resheight),
                                      (1.5\*reswidth, \-resheight),
                                      (2.5\*reswidth, resheight),
                                      (3.5\*reswidth, \-resheight),
                                      (4.5\*reswidth, resheight),
                                      (5.5\*reswidth, \-resheight),
                                      (6\*reswidth, 0)\]))

The resistor is made of one path. reswidth and resheight are constants that define the height and width of the resistor zigzag (and are referenced by several other elements too). Browse the source code in the Schemdraw.elements submodule to see the definitions of the other built-in elements.

#### Flux Capacitor Example[¶](#flux-capacitor-example "Link to this heading")

For an example, let’s make a flux capacitor circuit element.

Since everyone knows a flux-capacitor has three branches, we should subclass the standard [`schemdraw.elements.Element`](index.html#schemdraw.elements.Element "schemdraw.elements.Element") class instead of [`schemdraw.elements.Element2Term`](index.html#schemdraw.elements.Element2Term "schemdraw.elements.Element2Term"). Start by importing the Segments and define the class name and \_\_init\_\_ function:

from schemdraw.segments import \*

class FluxCapacitor(Element):
    def \_\_init\_\_(self, \*d, \*\*kwargs):
        super().\_\_init\_\_(\*d, \*\*kwargs)

The d and kwargs are passed to super to initialize the Element.

We want a dot in the center of our flux capacitor, so start by adding a SegmentCircle. The fclen and radius variables could be set as arguments to the \_\_init\_\_ for the user to adjust, if desired, but here they are defined as constants in the \_\_init\_\_.

fclen \= 0.5
radius \= 0.075
self.segments.append(SegmentCircle((0, 0), radius))

Next, add the paths as Segment instances, which are drawn as lines. The flux capacitor will have three paths, all extending from the center dot:

self.segments.append(Segment(\[(0, 0), (0, \-fclen\*1.41)\]))
self.segments.append(Segment(\[(0, 0), (fclen, fclen)\]))
self.segments.append(Segment(\[(0, 0), (\-fclen, fclen)\]))

And at the end of each path is an open circle. Append three more SegmentCircle instances. By specifying fill=None the SegmentCircle will always remain unfilled regardless of any fill arguments provided to Drawing or FluxCapacitor.

self.segments.append(SegmentCircle((0, \-fclen\*1.41), 0.2, fill\=None))
self.segments.append(SegmentCircle((fclen, fclen), 0.2, fill\=None))
self.segments.append(SegmentCircle((\-fclen, fclen), 0.2, fill\=None))

Finally, we need to define anchor points so that other elements can be connected to the right places. Here, they’re called p1, p2, and p3 for lack of better names (what do you call the inputs to a flux capacitor?) Add these to the self.anchors dictionary.

self.anchors\['p1'\] \= (\-fclen, fclen)
self.anchors\['p2'\] \= (fclen, fclen)
self.anchors\['p3'\] \= (0, \-fclen\*1.41)

Here’s the Flux Capacitor class all in one:

class FluxCapacitor(elm.Element):
    def \_\_init\_\_(self, \*d, \*\*kwargs):
        super().\_\_init\_\_(\*d, \*\*kwargs)
        radius \= 0.075
        fclen \= 0.5
        self.segments.append(SegmentCircle((0, 0), radius))
        self.segments.append(Segment(\[(0, 0), (0, \-fclen\*1.41)\]))
        self.segments.append(Segment(\[(0, 0), (fclen, fclen)\]))
        self.segments.append(Segment(\[(0, 0), (\-fclen, fclen)\]))
        self.segments.append(SegmentCircle((0, \-fclen\*1.41), 0.2, fill\=None))
        self.segments.append(SegmentCircle((fclen, fclen), 0.2, fill\=None))
        self.segments.append(SegmentCircle((\-fclen, fclen), 0.2, fill\=None))
        self.anchors\['p1'\] \= (\-fclen, fclen)
        self.anchors\['p2'\] \= (fclen, fclen)
        self.anchors\['p3'\] \= (0, \-fclen\*1.41)

Try it out:

FluxCapacitor()

![_images/customizing_3_0.svg](_images/customizing_3_0.svg)

### Segment objects[¶](#segment-objects "Link to this heading")

After an element is added to a drawing, the [`schemdraw.segments.Segment`](index.html#schemdraw.segments.Segment "schemdraw.segments.Segment") objects defining it are accessible in the segments attribute list of the Element. For even more control over customizing individual pieces of an element, the parameters of a Segment can be changed.

d += (n := logic.Nand())
n.segments\[1\].color \= 'red'
n.segments\[1\].zorder \= 5  \# Put the bubble on top

![_images/customizing_6_0.svg](_images/customizing_6_0.svg)

### Matplotlib axis[¶](#matplotlib-axis "Link to this heading")

When using the Matplotlib backend (the default), a final customization option is to use the Matplotlib figure and add to it. A `schemdraw.Figure` is returned from the draw method, which contains fig and ax attributes holding the Matplotlib figure.

schemdraw.use('matplotlib')
d \= schemdraw.Drawing()
d.add(elm.Resistor())
schemfig \= d.draw()
schemfig.ax.axvline(.5, color\='purple', ls\='--')
schemfig.ax.axvline(2.5, color\='orange', ls\='-', lw\=3);
display(schemfig)

![_images/customizing_7_0.svg](_images/customizing_7_0.svg)

Class Definitions[¶](#class-definitions "Link to this heading")
---------------------------------------------------------------

### Drawing[¶](#drawing "Link to this heading")

_class_ schemdraw.Drawing(_canvas: Backends | xml.etree.ElementTree.Element | matplotlib.pyplot.Axes \= None_, _file: str \= None_, _show: bool \= True_, _\*\*kwargs_)[¶](#schemdraw.Drawing "Link to this definition")

A schematic drawing

See schemdraw.config method for argument defaults

Parameters:

*   **canvas** – Canvas to draw on when using Drawing context manager. Can be string ‘matplotlib’ or ‘svg’ to create new canvas with these backends, or an instance of a matplotlib axis, or an instance of xml.etree.ElementTree containing SVG. Default is value set by schemdraw.use().
    
*   **file** – optional filename to save on exiting context manager or calling draw method.
    
*   **show** – Show the drawing after exiting context manager
    

here[¶](#schemdraw.Drawing.here "Link to this definition")

(xy tuple) Current drawing position. The next element will be added at this position unless specified otherwise.

theta[¶](#schemdraw.Drawing.theta "Link to this definition")

(float) Current drawing angle, in degrees. The next element will be added with this angle unless specified otherwise.

add(_element: [Element](index.html#schemdraw.elements.Element "schemdraw.elements.elements.Element")_) → [Element](index.html#schemdraw.elements.Element "schemdraw.elements.elements.Element")[¶](#schemdraw.Drawing.add "Link to this definition")

Add an element to the drawing.

Parameters:

**element** – The element to add.

add\_elements(_\*elements: [Element](index.html#schemdraw.elements.Element "schemdraw.elements.elements.Element")_) → None[¶](#schemdraw.Drawing.add_elements "Link to this definition")

Add multiple elements to the drawing

config(_unit: float \= None_, _inches\_per\_unit: float \= None_, _fontsize: float \= None_, _font: str \= None_, _color: str \= None_, _lw: float \= None_, _ls: Literal\['-', ':', '--', '-.'\] \= None_, _fill: str \= None_, _bgcolor: str \= None_, _margin: float \= None_) → None[¶](#schemdraw.Drawing.config "Link to this definition")

Set Drawing configuration, overriding schemdraw global config.

Parameters:

*   **unit** – Full length of a 2-terminal element. Inner zig-zag portion of a resistor is 1.0 units.
    
*   **inches\_per\_unit** – Inches per drawing unit for setting drawing scale
    
*   **fontsize** – Default font size for text labels
    
*   **font** – Default font family for text labels
    
*   **color** – Default color name or RGB (0-1) tuple
    
*   **lw** – Default line width for elements
    
*   **ls** – Default line style
    
*   **fill** – Deault fill color for closed elements
    

margin: White space around the drawing in drawing units

draw(_showframe: bool \= False_, _show: bool \= True_, _canvas\=None_, _backend: Literal\['svg', 'matplotlib'\] \= None_)[¶](#schemdraw.Drawing.draw "Link to this definition")

Draw the schematic

Parameters:

*   **showframe** – Show axis frame. Useful for debugging a drawing.
    
*   **show** – Show the schematic in a GUI popup window (when outside of a Jupyter inline environment)
    
*   **canvas** – ‘matplotlib’, ‘svg’, or Axis instance to draw on
    
*   **backend** (_deprecated_) – ‘matplotlib’ or ‘svg’
    

Returns:

schemdraw Figure object

get\_bbox() → BBox[¶](#schemdraw.Drawing.get_bbox "Link to this definition")

Get drawing bounding box

get\_imagedata(_fmt: ImageFormat | Literal\['eps', 'jpg', 'pdf', 'pgf', 'png', 'ps', 'raw', 'rgba', 'svg', 'tif'\] \= 'svg'_) → bytes[¶](#schemdraw.Drawing.get_imagedata "Link to this definition")

Get image data as bytes array

Parameters:

**fmt** – Format or file extension of the image type. SVG backend only supports ‘svg’ format.

Returns:

Image data as bytes

get\_segments() → list\[[Segment](index.html#schemdraw.segments.Segment "schemdraw.segments.Segment") | [SegmentText](index.html#schemdraw.segments.SegmentText "schemdraw.segments.SegmentText") | [SegmentPoly](index.html#schemdraw.segments.SegmentPoly "schemdraw.segments.SegmentPoly") | [SegmentArc](index.html#schemdraw.segments.SegmentArc "schemdraw.segments.SegmentArc") | [SegmentCircle](index.html#schemdraw.segments.SegmentCircle "schemdraw.segments.SegmentCircle") | [SegmentBezier](index.html#schemdraw.segments.SegmentBezier "schemdraw.segments.SegmentBezier")\][¶](#schemdraw.Drawing.get_segments "Link to this definition")

Get flattened list of all segments in the drawing

interactive(_interactive: bool \= True_)[¶](#schemdraw.Drawing.interactive "Link to this definition")

Enable interactive mode (matplotlib backend only). Matplotlib must also be set to interactive with plt.ion().

move(_dx: float \= 0_, _dy: float \= 0_) → None[¶](#schemdraw.Drawing.move "Link to this definition")

Move the current drawing position

Parameters:

*   **dx** – change in x position
    
*   **dy** – change in y position
    

move\_from(_ref: Point_, _dx: float \= 0_, _dy: float \= 0_, _theta: float \= None_) → None[¶](#schemdraw.Drawing.move_from "Link to this definition")

Move drawing position relative to the reference point. Change drawing theta if provided.

pop() → None[¶](#schemdraw.Drawing.pop "Link to this definition")

Pop/load the drawing state. Location and angle are returned to previously pushed state.

push() → None[¶](#schemdraw.Drawing.push "Link to this definition")

Push/save the drawing state. Drawing.here and Drawing.theta are saved.

save(_fname: str_, _transparent: bool \= True_, _dpi: float \= 72_) → None[¶](#schemdraw.Drawing.save "Link to this definition")

Save figure to a file

Parameters:

*   **fname** – Filename to save. In Matplotlib backend, the file type is automatically determined from extension (png, svg, jpg). SVG backend only supports saving SVG format.
    
*   **transparent** – Save as transparent background, if available
    
*   **dpi** – Dots-per-inch for raster formats
    

set\_anchor(_name: str_) → None[¶](#schemdraw.Drawing.set_anchor "Link to this definition")

Define a Drawing anchor at the current drawing position

undo() → None[¶](#schemdraw.Drawing.undo "Link to this definition")

Removes previously added element

### Element[¶](#element "Link to this heading")

_class_ schemdraw.elements.Element(_\*d_, _\*\*kwargs_)[¶](#schemdraw.elements.Element "Link to this definition")

Standard circuit element.

Keyword Arguments are equivalent to calling setter methods.

Parameters:

**d** – Drawing direction (‘up’, ‘down’, ‘left’, ‘right’)

anchors[¶](#schemdraw.elements.Element.anchors "Link to this definition")

Dictionary of anchor positions in element coordinates

absanchors[¶](#schemdraw.elements.Element.absanchors "Link to this definition")

Dictionary of anchor positions in absolute drawing coordinates

segments[¶](#schemdraw.elements.Element.segments "Link to this definition")

List of drawing primitives making up the element

transform[¶](#schemdraw.elements.Element.transform "Link to this definition")

Transformation from element to drawing coordinates

Anchor names are dynmically added as attributes after placing the element in a Drawing.

anchor(_anchor: str_) → [Element](index.html#schemdraw.elements.Element "schemdraw.elements.elements.Element")[¶](#schemdraw.elements.Element.anchor "Link to this definition")

Specify anchor for placement. The anchor will be aligned with the position specified by at() method.

at(_xy: Tuple\[float, float\] | Point | tuple\[[Element](index.html#schemdraw.elements.Element "schemdraw.elements.elements.Element"), str\]_, _dx: float \= 0_, _dy: float \= 0_) → [Element](index.html#schemdraw.elements.Element "schemdraw.elements.elements.Element")[¶](#schemdraw.elements.Element.at "Link to this definition")

Set the element xy position

Parameters:

**xy** – (x,y) position or tuple of (Element, anchorname)

color(_color: str_) → [Element](index.html#schemdraw.elements.Element "schemdraw.elements.elements.Element")[¶](#schemdraw.elements.Element.color "Link to this definition")

Sets the element color

Parameters:

**color** – color name or hex value (ie ‘#FFFFFF’)

down() → [Element](index.html#schemdraw.elements.Element "schemdraw.elements.elements.Element")[¶](#schemdraw.elements.Element.down "Link to this definition")

Set the direction to down

drop(_drop: str | Point_) → [Element](index.html#schemdraw.elements.Element "schemdraw.elements.elements.Element")[¶](#schemdraw.elements.Element.drop "Link to this definition")

Set the drop position - where to leave the current drawing position after placing this element

fill(_color: bool | str \= True_) → [Element](index.html#schemdraw.elements.Element "schemdraw.elements.elements.Element")[¶](#schemdraw.elements.Element.fill "Link to this definition")

Sets the element fill color.

Parameters:

*   **color** – Color string name or hex value, or
    
*   **color.** (_True to fill with the element line_) –
    

flip() → [Element](index.html#schemdraw.elements.Element "schemdraw.elements.elements.Element")[¶](#schemdraw.elements.Element.flip "Link to this definition")

Apply flip up/down

get\_bbox(_transform\=False_, _includetext\=True_)[¶](#schemdraw.elements.Element.get_bbox "Link to this definition")

Get element bounding box

Parameters:

*   **transform** – Apply the element transform to the bbox to get bounds in Drawing coordinates
    
*   **includetext** – Consider text when calculating bounding box. Text width and height can vary by font, so this produces an estimate of bounds.
    

Returns:

Corners of the bounding box, (xmin, ymin, xmax, ymax)

hold() → [Element](index.html#schemdraw.elements.Element "schemdraw.elements.elements.Element")[¶](#schemdraw.elements.Element.hold "Link to this definition")

Do not move the Drawing here position after placing this element

label(_label: str | Sequence\[str\]_, _loc: Literal\['top', 'bot', 'lft', 'rgt', 'bottom', 'left', 'right', 'L', 'R', 'T', 'B'\] | str \= None_, _ofst: Tuple\[float, float\] | Point | float | None \= None_, _halign: Literal\['center', 'left', 'right'\] \= None_, _valign: Literal\['center', 'top', 'bottom'\] \= None_, _rotate: bool | float \= False_, _fontsize: float \= None_, _font: str \= None_, _mathfont: str \= None_, _color: str \= None_)[¶](#schemdraw.elements.Element.label "Link to this definition")

Add a label to the Element.

Parameters:

*   **label** – The text string or list of strings. If list, each string will be evenly spaced along the element (e.g. \[‘-’, ‘V’, ‘+’\])
    
*   **loc** – Label position within the Element. Either (‘top’, ‘bottom’, ‘left’, ‘right’), or the name of an anchor within the Element.
    
*   **ofst** – Offset from default label position
    
*   **halign** – Horizontal text alignment (‘center’, ‘left’, ‘right’)
    
*   **valign** – Vertical text alignment (‘center’, ‘top’, ‘bottom’)
    
*   **rotate** – True to rotate label with element, or specify rotation angle in degrees
    
*   **fontsize** – Size of label font
    
*   **font** – Name/font-family of label text
    
*   **mathfont** – Name/font-family of math text
    
*   **color** – Color of label
    

left() → [Element](index.html#schemdraw.elements.Element "schemdraw.elements.elements.Element")[¶](#schemdraw.elements.Element.left "Link to this definition")

Set the direction to left

linestyle(_ls: Literal\['-', ':', '--', '-.'\]_) → [Element](index.html#schemdraw.elements.Element "schemdraw.elements.elements.Element")[¶](#schemdraw.elements.Element.linestyle "Link to this definition")

Sets the element line style

Parameters:

**ls** – Line style (‘-’, ‘:’, ‘–’, ‘-.’).

linewidth(_lw: float_) → [Element](index.html#schemdraw.elements.Element "schemdraw.elements.elements.Element")[¶](#schemdraw.elements.Element.linewidth "Link to this definition")

Sets the element line width

Parameters:

**lw** – Line width

reverse() → [Element](index.html#schemdraw.elements.Element "schemdraw.elements.elements.Element")[¶](#schemdraw.elements.Element.reverse "Link to this definition")

Apply reverse left/right

right() → [Element](index.html#schemdraw.elements.Element "schemdraw.elements.elements.Element")[¶](#schemdraw.elements.Element.right "Link to this definition")

Set the direction to right

scale(_scale: float \= 1_) → [Element](index.html#schemdraw.elements.Element "schemdraw.elements.elements.Element")[¶](#schemdraw.elements.Element.scale "Link to this definition")

Apply scale/zoom factor to element

style(_color: str \= None_, _fill: str \= None_, _ls: Literal\['-', ':', '--', '-.'\] \= None_, _lw: float \= None_) → [Element](index.html#schemdraw.elements.Element "schemdraw.elements.elements.Element")[¶](#schemdraw.elements.Element.style "Link to this definition")

Apply all style parameters

Parameters:

*   **color** – Color string or hex value
    
*   **fill** – Color string or hex
    
*   **ls** – Line style (‘-’, ‘:’, ‘–’, ‘-.’)
    
*   **lw** – Line width
    

theta(_theta: float_) → [Element](index.html#schemdraw.elements.Element "schemdraw.elements.elements.Element")[¶](#schemdraw.elements.Element.theta "Link to this definition")

Set the drawing direction angle in degrees

up() → [Element](index.html#schemdraw.elements.Element "schemdraw.elements.elements.Element")[¶](#schemdraw.elements.Element.up "Link to this definition")

Set the direction to up

zorder(_zorder: int_) → [Element](index.html#schemdraw.elements.Element "schemdraw.elements.elements.Element")[¶](#schemdraw.elements.Element.zorder "Link to this definition")

Sets the element zorder. Higher zorders will be drawn above lower zorder elements.

### Element2Term[¶](#element2term "Link to this heading")

_class_ schemdraw.elements.Element2Term(_\*d_, _\*\*kwargs_)[¶](#schemdraw.elements.Element2Term "Link to this definition")

Two terminal element. The element leads can be automatically extended to the start and ending positions.

Anchors:

*   start
    
*   center
    
*   end
    

dot(_open: bool \= False_) → [Element2Term](index.html#schemdraw.elements.Element2Term "schemdraw.elements.elements.Element2Term")[¶](#schemdraw.elements.Element2Term.dot "Link to this definition")

Add a dot to the end of the element

down(_length: float \= None_) → [Element](index.html#schemdraw.elements.Element "schemdraw.elements.elements.Element")[¶](#schemdraw.elements.Element2Term.down "Link to this definition")

Set the direction to down

endpoints(_start: Tuple\[float, float\] | Point_, _end: Tuple\[float, float\] | Point_) → [Element2Term](index.html#schemdraw.elements.Element2Term "schemdraw.elements.elements.Element2Term")[¶](#schemdraw.elements.Element2Term.endpoints "Link to this definition")

Sets absolute endpoints of element

idot(_open: bool \= False_) → [Element2Term](index.html#schemdraw.elements.Element2Term "schemdraw.elements.elements.Element2Term")[¶](#schemdraw.elements.Element2Term.idot "Link to this definition")

Add a dot to the input/start of the element

left(_length: float \= None_) → [Element](index.html#schemdraw.elements.Element "schemdraw.elements.elements.Element")[¶](#schemdraw.elements.Element2Term.left "Link to this definition")

Set the direction to left

length(_length: float_) → [Element2Term](index.html#schemdraw.elements.Element2Term "schemdraw.elements.elements.Element2Term")[¶](#schemdraw.elements.Element2Term.length "Link to this definition")

Sets total length of element

right(_length: float \= None_) → [Element](index.html#schemdraw.elements.Element "schemdraw.elements.elements.Element")[¶](#schemdraw.elements.Element2Term.right "Link to this definition")

Set the direction to right

to(_xy: Tuple\[float, float\] | Point_, _dx: float \= 0_, _dy: float \= 0_) → [Element2Term](index.html#schemdraw.elements.Element2Term "schemdraw.elements.elements.Element2Term")[¶](#schemdraw.elements.Element2Term.to "Link to this definition")

Sets ending position of element

Parameters:

*   **xy** – Ending position of element
    
*   **dx** – X-offset from xy position
    
*   **dy** – Y-offset from xy position
    

tox(_x: float | Tuple\[float, float\] | Point | [Element](index.html#schemdraw.elements.Element "schemdraw.elements.elements.Element")_) → [Element2Term](index.html#schemdraw.elements.Element2Term "schemdraw.elements.elements.Element2Term")[¶](#schemdraw.elements.Element2Term.tox "Link to this definition")

Sets ending x-position of element (for horizontal elements)

toy(_y: float | Tuple\[float, float\] | Point | [Element](index.html#schemdraw.elements.Element "schemdraw.elements.elements.Element")_) → [Element2Term](index.html#schemdraw.elements.Element2Term "schemdraw.elements.elements.Element2Term")[¶](#schemdraw.elements.Element2Term.toy "Link to this definition")

Sets ending y-position of element (for vertical elements)

up(_length: float \= None_) → [Element](index.html#schemdraw.elements.Element "schemdraw.elements.elements.Element")[¶](#schemdraw.elements.Element2Term.up "Link to this definition")

Set the direction to up

### ElementDrawing[¶](#elementdrawing "Link to this heading")

_class_ schemdraw.elements.ElementDrawing(_drawing_, _\*\*kwargs_)[¶](#schemdraw.elements.ElementDrawing "Link to this definition")

Create an element from a Drawing

Parameters:

**drawing** – The Drawing instance to convert to an element

### Element Style[¶](#element-style "Link to this heading")

schemdraw.elements.style(_style_)[¶](#schemdraw.elements.style "Link to this definition")

Set global element style

Parameters:

**style** – dictionary of {elementname: Element} to change the element module namespace. Use elements.STYLE\_US or elements.STYLE\_IEC to define U.S. or European/IEC element styles.

schemdraw.config(_unit: float \= 3.0_, _inches\_per\_unit: float \= 0.5_, _lblofst: float \= 0.1_, _fontsize: float \= 14.0_, _font: str \= 'sans-serif'_, _color: str \= 'black'_, _lw: float \= 2.0_, _ls: Literal\['-', ':', '--', '-.'\] \= '-'_, _fill: str \= None_, _bgcolor: str \= None_, _margin: float \= 0.1_) → None[¶](#schemdraw.config "Link to this definition")

Set global schemdraw style configuration

Parameters:

*   **unit** – Full length of a 2-terminal element. Inner zig-zag portion of a resistor is 1.0 units.
    
*   **inches\_per\_unit** – Inches per drawing unit for setting drawing scale
    
*   **lblofst** – Default offset between element and its label
    
*   **fontsize** – Default font size for text labels
    
*   **font** – Default font family for text labels
    
*   **color** – Default color name or RGB (0-1) tuple
    
*   **lw** – Default line width for elements
    
*   **ls** – Default line style
    
*   **fill** – Deault fill color for closed elements
    
*   **margin** – White space around the drawing in drawing units
    

schemdraw.theme(_theme\='default'_)[¶](#schemdraw.theme "Link to this definition")

Set schemdraw theme (line color and background color). Themes match those in jupyter-themes package ([https://github.com/dunovank/jupyter-themes](https://github.com/dunovank/jupyter-themes)).

Available themes:

*   default (black on white)
    
*   dark (white on black)
    
*   solarizedd
    
*   solarizedl
    
*   onedork
    
*   oceans16
    
*   monokai
    
*   gruvboxl
    
*   gruvboxd
    
*   grade3
    
*   chesterish
    

schemdraw.use(_backend: Literal\['svg', 'matplotlib'\] \= 'matplotlib'_) → None[¶](#schemdraw.use "Link to this definition")

Change default backend, either ‘matplotlib’ or ‘svg’

### Segment Drawing Primitives[¶](#module-schemdraw.segments "Link to this heading")

Schemdraw drawing segments.

Each element is made up of one or more segments that define drawing primitives.

_class_ schemdraw.segments.Segment(_path: Sequence\[Tuple\[float, float\] | Point\]_, _color: str \= None_, _lw: float \= None_, _ls: Literal\['-', ':', '--', '-.'\] \= None_, _capstyle: Literal\['butt', 'round', 'square', 'projecting'\] \= None_, _joinstyle: Literal\['bevel', 'miter', 'round'\] \= None_, _fill: str \= None_, _arrow: str \= None_, _arrowwidth: float \= 0.15_, _arrowlength: float \= 0.25_, _clip: BBox \= None_, _zorder: int \= None_, _visible: bool \= True_)[¶](#schemdraw.segments.Segment "Link to this definition")

A segment path

Parameters:

*   **path** – List of (x,y) coordinates making the path
    
*   **color** – Color for this segment
    
*   **lw** – Line width for the segment
    
*   **ls** – Line style for the segment ‘-’, ‘–’, ‘:’, etc.
    
*   **capstyle** – Capstyle for the segment: ‘butt’, ‘round’, ‘square’, (‘projecting’)
    
*   **joinstyle** – Joinstyle for the segment: ‘round’, ‘miter’, or ‘bevel’
    
*   **fill** – Color to fill if path is closed
    
*   **arrow** – Arrowhead specifier, such as ‘->’, ‘<-’, ‘<->’, ‘-o’, etc.
    
*   **arrowwidth** – Width of arrowhead
    
*   **arrowlength** – Length of arrowhead
    
*   **clip** – Bounding box to clip to
    
*   **zorder** – Z-order for segment
    
*   **visible** – Show the segment when drawn
    

doflip() → None[¶](#schemdraw.segments.Segment.doflip "Link to this definition")

Vertically flip the element

doreverse(_centerx: float_) → None[¶](#schemdraw.segments.Segment.doreverse "Link to this definition")

Reverse the path (flip horizontal about the center of the path)

draw(_fig_, _transform_, _\*\*style_) → None[¶](#schemdraw.segments.Segment.draw "Link to this definition")

Draw the segment

Parameters:

*   **fig** – schemdraw.Figure to draw on
    
*   **transform** – Transform to apply before drawing
    
*   **style** – Default style parameters
    

get\_bbox() → BBox[¶](#schemdraw.segments.Segment.get_bbox "Link to this definition")

Get bounding box (untransformed)

Returns:

(xmin, ymin, xmax, ymax)

Return type:

Bounding box limits

xform(_transform_, _\*\*style_) → [Segment](index.html#schemdraw.segments.Segment "schemdraw.segments.Segment")[¶](#schemdraw.segments.Segment.xform "Link to this definition")

Return a new Segment that has been transformed to its global position

Parameters:

*   **transform** – Transformation to apply
    
*   **style** – Style parameters from Element to apply as default
    

_class_ schemdraw.segments.SegmentArc(_center: Tuple\[float, float\] | Point_, _width: float_, _height: float_, _theta1: float \= 35_, _theta2: float \= \-35_, _arrow: Literal\['cw', 'ccw'\] \= None_, _angle: float \= 0_, _color: str \= None_, _lw: float \= None_, _ls: Literal\['-', ':', '--', '-.'\] \= None_, _clip: BBox \= None_, _zorder: int \= None_, _visible: bool \= True_)[¶](#schemdraw.segments.SegmentArc "Link to this definition")

An elliptical arc drawing segment

Parameters:

*   **center** – Center of the arc ellipse
    
*   **width** – Width of the arc ellipse
    
*   **height** – Height of the arc ellipse
    
*   **theta1** – Starting angle in degrees
    
*   **theta2** – Ending angle in degrees
    
*   **arrow** – Direction of arrowhead (‘cw’ or ‘ccw’)
    
*   **angle** – Rotation of the ellipse defining the arc
    
*   **color** – Color for this segment
    
*   **lw** – Line width for the segment
    
*   **ls** – Line style for the segment
    
*   **clip** – Bounding box to clip to
    
*   **zorder** – Z-order for segment
    
*   **visible** – Show the segment when drawn
    

doflip() → None[¶](#schemdraw.segments.SegmentArc.doflip "Link to this definition")

Vertically flip the element

doreverse(_centerx: float_) → None[¶](#schemdraw.segments.SegmentArc.doreverse "Link to this definition")

Reverse the path (flip horizontal about the centerx point)

draw(_fig_, _transform_, _\*\*style_) → None[¶](#schemdraw.segments.SegmentArc.draw "Link to this definition")

Draw the segment

Parameters:

*   **fig** – schemdraw.Figure to draw on
    
*   **transform** – Transform to apply before drawing
    
*   **style** – Default style parameters
    

get\_bbox() → BBox[¶](#schemdraw.segments.SegmentArc.get_bbox "Link to this definition")

Get bounding box (untransformed)

Returns:

Bounding box limits (xmin, ymin, xmax, ymax)

xform(_transform_, _\*\*style_) → [SegmentArc](index.html#schemdraw.segments.SegmentArc "schemdraw.segments.SegmentArc")[¶](#schemdraw.segments.SegmentArc.xform "Link to this definition")

Return a new Segment that has been transformed to its global position

Parameters:

*   **transform** – Transformation to apply
    
*   **style** – Style parameters from Element to apply as default
    

_class_ schemdraw.segments.SegmentArrow(_tail: Tuple\[float, float\] | Point_, _head: Tuple\[float, float\] | Point_, _headwidth: float \= None_, _headlength: float \= None_, _color: str \= None_, _lw: float \= None_, _clip: BBox \= None_, _ref: Literal\['start', 'end'\] \= None_, _zorder: int \= None_)[¶](#schemdraw.segments.SegmentArrow "Link to this definition")

Arrow Segment

\[DEPRECATED - use Segment with arrow parameter instead\]

_class_ schemdraw.segments.SegmentBezier(_p: Sequence\[Tuple\[float, float\] | Point\]_, _color: str \= None_, _lw: float \= None_, _ls: Literal\['-', ':', '--', '-.'\] \= None_, _capstyle: Literal\['butt', 'round', 'square', 'projecting'\] \= None_, _arrow: str \= None_, _arrowlength: float \= 0.25_, _arrowwidth: float \= 0.15_, _clip: BBox \= None_, _zorder: int \= None_, _visible: bool \= True_)[¶](#schemdraw.segments.SegmentBezier "Link to this definition")

Quadratic or Cubic Bezier curve segment

Parameters:

*   **p** – control points (3 or 4)
    
*   **color** – Color for this segment
    
*   **lw** – Line width for the segment
    
*   **ls** – Line style for the segment ‘-’, ‘–’, ‘:’, etc.
    
*   **capstyle** – Capstyle for the segment: ‘butt’, ‘round’, ‘square’, (‘projecting’)
    
*   **joinstyle** – Joinstyle for the segment: ‘round’, ‘miter’, or ‘bevel’
    
*   **fill** – Color to fill if path is closed
    
*   **arrow** – Arrowhead specifier, such as ‘->’, ‘<-’, or ‘<->’
    
*   **arrowwidth** – Width of arrowhead
    
*   **arrowlength** – Length of arrowhead
    
*   **clip** – Bounding box to clip to
    
*   **zorder** – Z-order for segment
    
*   **visible** – Show the segment when drawn
    

doflip() → None[¶](#schemdraw.segments.SegmentBezier.doflip "Link to this definition")

Vertically flip the element

doreverse(_centerx: float_) → None[¶](#schemdraw.segments.SegmentBezier.doreverse "Link to this definition")

Reverse the path (flip horizontal about the centerx point)

draw(_fig_, _transform_, _\*\*style_) → None[¶](#schemdraw.segments.SegmentBezier.draw "Link to this definition")

Draw the segment

Parameters:

*   **fig** – schemdraw.Figure to draw on
    
*   **transform** – Transform to apply before drawing
    
*   **style** – Default style parameters
    

get\_bbox() → BBox[¶](#schemdraw.segments.SegmentBezier.get_bbox "Link to this definition")

Get bounding box (untransformed)

Returns:

Bounding box limits (xmin, ymin, xmax, ymax)

xform(_transform_, _\*\*style_) → [SegmentBezier](index.html#schemdraw.segments.SegmentBezier "schemdraw.segments.SegmentBezier")[¶](#schemdraw.segments.SegmentBezier.xform "Link to this definition")

Return a new Segment that has been transformed to its global position

Parameters:

*   **transform** – Transformation to apply
    
*   **style** – Style parameters from Element to apply as default
    

_class_ schemdraw.segments.SegmentCircle(_center: Tuple\[float, float\] | Point_, _radius: float_, _color: str \= None_, _lw: float \= None_, _ls: Literal\['-', ':', '--', '-.'\] \= None_, _fill: bool | str | None \= None_, _clip: BBox \= None_, _zorder: int \= None_, _ref: Literal\['start', 'end'\] \= None_, _visible: bool \= True_)[¶](#schemdraw.segments.SegmentCircle "Link to this definition")

A circle drawing segment

Parameters:

*   **center** – (x, y) center of the circle
    
*   **radius** – Radius of the circle
    
*   **color** – Color for this segment
    
*   **lw** – Line width for the segment
    
*   **ls** – Line style for the segment
    
*   **fill** – Color to fill if path is closed. True -> fill with element color.
    
*   **clip** – Bounding box to clip to
    
*   **zorder** – Z-order for segment
    
*   **ref** – Flip reference \[‘start’, ‘end’, None\].
    
*   **visible** – Show the segment when drawn
    

doflip() → None[¶](#schemdraw.segments.SegmentCircle.doflip "Link to this definition")

Flip the segment up/down

doreverse(_centerx: float_) → None[¶](#schemdraw.segments.SegmentCircle.doreverse "Link to this definition")

Reverse the path (flip horizontal about the centerx point)

draw(_fig_, _transform_, _\*\*style_) → None[¶](#schemdraw.segments.SegmentCircle.draw "Link to this definition")

Draw the segment

Parameters:

*   **fig** – schemdraw.Figure to draw on
    
*   **transform** – Transform to apply before drawing
    
*   **style** – Default style parameters
    

get\_bbox() → BBox[¶](#schemdraw.segments.SegmentCircle.get_bbox "Link to this definition")

Get bounding box (untransformed)

Returns:

Bounding box limits (xmin, ymin, xmax, ymax)

xform(_transform_, _\*\*style_) → [SegmentCircle](index.html#schemdraw.segments.SegmentCircle "schemdraw.segments.SegmentCircle")[¶](#schemdraw.segments.SegmentCircle.xform "Link to this definition")

Return a new Segment that has been transformed to its global position

Parameters:

*   **transform** – Transformation to apply
    
*   **style** – Style parameters from Element to apply as default
    

_class_ schemdraw.segments.SegmentPoly(_verts: Sequence\[Tuple\[float, float\] | Point\]_, _closed: bool \= True_, _cornerradius: float \= 0_, _color: str \= None_, _fill: str \= None_, _lw: float \= None_, _ls: Literal\['-', ':', '--', '-.'\] \= None_, _hatch: bool \= False_, _joinstyle: Literal\['bevel', 'miter', 'round'\] \= None_, _capstyle: Literal\['butt', 'round', 'square', 'projecting'\] \= None_, _clip: BBox \= None_, _zorder: int \= None_, _visible: bool \= True_)[¶](#schemdraw.segments.SegmentPoly "Link to this definition")

A polygon segment

Parameters:

*   **xy** – List of (x,y) coordinates making the polygon
    
*   **closed** – Draw a closed polygon (default True)
    
*   **cornerradius** – Round the corners to this radius (0 for no rounding)
    
*   **color** – Color for this segment
    
*   **fill** – Color to fill if path is closed
    
*   **lw** – Line width for the segment
    
*   **ls** – Line style for the segment
    
*   **hatch** – Show hatch lines
    
*   **capstyle** – Capstyle for the segment: ‘butt’, ‘round’, ‘square’, (‘projecting’)
    
*   **joinstyle** – Joinstyle for the segment: ‘round’, ‘miter’, or ‘bevel’
    
*   **clip** – Bounding box to clip to
    
*   **zorder** – Z-order for segment
    
*   **visible** – Show the segment when drawn
    

doflip() → None[¶](#schemdraw.segments.SegmentPoly.doflip "Link to this definition")

Vertically flip the element

doreverse(_centerx: float_) → None[¶](#schemdraw.segments.SegmentPoly.doreverse "Link to this definition")

Reverse the path (flip horizontal about the centerx point)

draw(_fig_, _transform_, _\*\*style_) → None[¶](#schemdraw.segments.SegmentPoly.draw "Link to this definition")

Draw the segment

Parameters:

*   **fig** – schemdraw.Figure to draw on
    
*   **transform** – Transform to apply before drawing
    
*   **style** – Default style parameters
    

get\_bbox() → BBox[¶](#schemdraw.segments.SegmentPoly.get_bbox "Link to this definition")

Get bounding box (untransformed)

Returns:

Bounding box limits (xmin, ymin, xmax, ymax)

xform(_transform_, _\*\*style_) → [SegmentPoly](index.html#schemdraw.segments.SegmentPoly "schemdraw.segments.SegmentPoly")[¶](#schemdraw.segments.SegmentPoly.xform "Link to this definition")

Return a new Segment that has been transformed to its global position

Parameters:

*   **transform** – Transformation to apply
    
*   **style** – Style parameters from Element to apply as default
    

_class_ schemdraw.segments.SegmentText(_pos: Tuple\[float, float\] | Point_, _label: str_, _align: Tuple\[Literal\['center', 'left', 'right'\], Literal\['center', 'top', 'bottom'\]\] \= None_, _rotation: float \= None_, _rotation\_mode: Literal\['anchor', 'default'\] \= None_, _rotation\_global: bool \= True_, _color: str \= None_, _fontsize: float \= 14_, _font: str \= None_, _mathfont: str \= None_, _clip: BBox \= None_, _zorder: int \= None_, _visible: bool \= True_)[¶](#schemdraw.segments.SegmentText "Link to this definition")

A text drawing segment

Parameters:

*   **pos** – (x, y) coordinates for text
    
*   **label** – Text to draw
    
*   **align** – Tuple of (horizontal, vertical) alignment where horizontal is (‘center’, ‘left’, ‘right’) and vertical is (‘center’, ‘top’, ‘bottom’)
    
*   **rotation** – Rotation angle in degrees
    
*   **rotation\_mode** – See Matplotlib documentation. ‘anchor’ or ‘default’.
    
*   **rotation\_global** – Lock rotation to world rather than component. Defaults to True
    
*   **color** – Color for this segment
    
*   **fontsize** – Font size
    
*   **font** – Font name/family
    
*   **mathfont** – Math font name/family
    
*   **clip** – Bounding box to clip to
    
*   **zorder** – Z-order for segment
    
*   **visible** – Show the segment when drawn
    

doflip() → None[¶](#schemdraw.segments.SegmentText.doflip "Link to this definition")

Vertically flip the element

doreverse(_centerx: float_) → None[¶](#schemdraw.segments.SegmentText.doreverse "Link to this definition")

Reverse the path (flip horizontal about the centerx point)

draw(_fig_, _transform_, _\*\*style_) → None[¶](#schemdraw.segments.SegmentText.draw "Link to this definition")

Draw the segment

Parameters:

*   **fig** – schemdraw.Figure to draw on
    
*   **transform** – Transform to apply before drawing
    
*   **style** – Default style parameters
    

get\_bbox() → BBox[¶](#schemdraw.segments.SegmentText.get_bbox "Link to this definition")

Get bounding box (untransformed)

Returns:

Bounding box limits (xmin, ymin, xmax, ymax)

xform(_transform_, _\*\*style_) → [SegmentText](index.html#schemdraw.segments.SegmentText "schemdraw.segments.SegmentText")[¶](#schemdraw.segments.SegmentText.xform "Link to this definition")

Return a new Segment that has been transformed to its global position

Parameters:

*   **transform** – Transformation to apply
    
*   **style** – Style parameters from Element to apply as default
    

### Electrical Elements[¶](#electrical-elements "Link to this heading")

#### Two-Terminal Elements[¶](#module-schemdraw.elements.twoterm "Link to this heading")

Two-terminal element definitions

_class_ schemdraw.elements.twoterm.Breaker(_\*d_, _dots: bool \= True_, _\*\*kwargs_)[¶](#schemdraw.elements.twoterm.Breaker "Link to this definition")

Circuit breaker

Parameters:

**dots** – Show connection dots

_class_ schemdraw.elements.twoterm.CPE(_\*d_, _\*\*kwargs_)[¶](#schemdraw.elements.twoterm.CPE "Link to this definition")

Constant Phase Element

_class_ schemdraw.elements.twoterm.Capacitor(_flat plates_)[¶](#schemdraw.elements.twoterm.Capacitor "Link to this definition")

Parameters:

**polar** – Add polarity + sign

_class_ schemdraw.elements.twoterm.Capacitor2(_\*d_, _polar: bool \= False_, _\*\*kwargs_)[¶](#schemdraw.elements.twoterm.Capacitor2 "Link to this definition")

Capacitor (curved bottom plate)

Parameters:

**polar** – Add polarity + sign

_class_ schemdraw.elements.twoterm.CapacitorTrim(_\*d_, _\*\*kwargs_)[¶](#schemdraw.elements.twoterm.CapacitorTrim "Link to this definition")

Trim capacitor

_class_ schemdraw.elements.twoterm.CapacitorVar(_\*d_, _\*\*kwargs_)[¶](#schemdraw.elements.twoterm.CapacitorVar "Link to this definition")

Variable capacitor

_class_ schemdraw.elements.twoterm.Crystal(_\*d_, _\*\*kwargs_)[¶](#schemdraw.elements.twoterm.Crystal "Link to this definition")

Crystal oscillator

_class_ schemdraw.elements.twoterm.CurrentMirror(_\*d_, _\*\*kwargs_)[¶](#schemdraw.elements.twoterm.CurrentMirror "Link to this definition")

Current mirror with optional common terminal

Anchors:

*   scommon
    

_class_ schemdraw.elements.twoterm.Diac(_\*d_, _\*\*kwargs_)[¶](#schemdraw.elements.twoterm.Diac "Link to this definition")

Diac (diode for alternating current)

_class_ schemdraw.elements.twoterm.Diode(_\*d_, _\*\*kwargs_)[¶](#schemdraw.elements.twoterm.Diode "Link to this definition")

_class_ schemdraw.elements.twoterm.DiodeShockley(_\*d_, _\*\*kwargs_)[¶](#schemdraw.elements.twoterm.DiodeShockley "Link to this definition")

Shockley Diode

_class_ schemdraw.elements.twoterm.DiodeTunnel(_\*d_, _\*\*kwargs_)[¶](#schemdraw.elements.twoterm.DiodeTunnel "Link to this definition")

Tunnel Diode

schemdraw.elements.twoterm.Fuse[¶](#schemdraw.elements.twoterm.Fuse "Link to this definition")

alias of [`FuseIEEE`](#schemdraw.elements.twoterm.FuseIEEE "schemdraw.elements.twoterm.FuseIEEE")

_class_ schemdraw.elements.twoterm.FuseIEC(_\*d_, _\*\*kwargs_)[¶](#schemdraw.elements.twoterm.FuseIEC "Link to this definition")

Fuse (IEC Style)

_class_ schemdraw.elements.twoterm.FuseIEEE(_\*d_, _\*\*kwargs_)[¶](#schemdraw.elements.twoterm.FuseIEEE "Link to this definition")

Fuse (IEEE Style)

_class_ schemdraw.elements.twoterm.FuseUS(_\*d_, _dots: bool \= True_, _\*\*kwargs_)[¶](#schemdraw.elements.twoterm.FuseUS "Link to this definition")

Fuse (U.S. Style)

Parameters:

**dots** – Show dots on connections to fuse

fill(_color: bool | str \= True_) → [Element](index.html#schemdraw.elements.Element "schemdraw.elements.elements.Element")[¶](#schemdraw.elements.twoterm.FuseUS.fill "Link to this definition")

Set element fill

_class_ schemdraw.elements.twoterm.Inductor(_\*d_, _\*\*kwargs_)[¶](#schemdraw.elements.twoterm.Inductor "Link to this definition")

_class_ schemdraw.elements.twoterm.Inductor2(_\*d_, _loops: int \= 4_, _\*\*kwargs_)[¶](#schemdraw.elements.twoterm.Inductor2 "Link to this definition")

Inductor, drawn as cycloid (loopy)

Parameters:

**loops** – Number of inductor loops

_class_ schemdraw.elements.twoterm.Josephson(_\*d_, _\*\*kwargs_)[¶](#schemdraw.elements.twoterm.Josephson "Link to this definition")

Josephson Junction

_class_ schemdraw.elements.twoterm.LED(_\*d_, _\*\*kwargs_)[¶](#schemdraw.elements.twoterm.LED "Link to this definition")

Light emitting diode

_class_ schemdraw.elements.twoterm.LED2(_\*d_, _\*\*kwargs_)[¶](#schemdraw.elements.twoterm.LED2 "Link to this definition")

Light emitting diode (curvy light lines)

_class_ schemdraw.elements.twoterm.Memristor(_\*d_, _\*\*kwargs_)[¶](#schemdraw.elements.twoterm.Memristor "Link to this definition")

Memristor (resistor with memory)

_class_ schemdraw.elements.twoterm.Memristor2(_\*d_, _\*\*kwargs_)[¶](#schemdraw.elements.twoterm.Memristor2 "Link to this definition")

Memristor (resistor with memory), alternate style

_class_ schemdraw.elements.twoterm.Norator(_\*args_, _\*\*kwargs_)[¶](#schemdraw.elements.twoterm.Norator "Link to this definition")

_class_ schemdraw.elements.twoterm.Nullator(_\*args_, _\*\*kwargs_)[¶](#schemdraw.elements.twoterm.Nullator "Link to this definition")

This element does not support filling

_class_ schemdraw.elements.twoterm.Photodiode(_\*d_, _\*\*kwargs_)[¶](#schemdraw.elements.twoterm.Photodiode "Link to this definition")

Photo-sensitive diode

schemdraw.elements.twoterm.Photoresistor[¶](#schemdraw.elements.twoterm.Photoresistor "Link to this definition")

alias of [`PhotoresistorIEEE`](#schemdraw.elements.twoterm.PhotoresistorIEEE "schemdraw.elements.twoterm.PhotoresistorIEEE")

schemdraw.elements.twoterm.PhotoresistorBox[¶](#schemdraw.elements.twoterm.PhotoresistorBox "Link to this definition")

alias of [`PhotoresistorIEC`](#schemdraw.elements.twoterm.PhotoresistorIEC "schemdraw.elements.twoterm.PhotoresistorIEC")

_class_ schemdraw.elements.twoterm.PhotoresistorIEC(_\*d_, _\*\*kwargs_)[¶](#schemdraw.elements.twoterm.PhotoresistorIEC "Link to this definition")

Photo-resistor (European style)

_class_ schemdraw.elements.twoterm.PhotoresistorIEEE(_\*d_, _\*\*kwargs_)[¶](#schemdraw.elements.twoterm.PhotoresistorIEEE "Link to this definition")

Photo-resistor (U.S. style)

schemdraw.elements.twoterm.PotBox[¶](#schemdraw.elements.twoterm.PotBox "Link to this definition")

alias of [`PotentiometerIEC`](#schemdraw.elements.twoterm.PotentiometerIEC "schemdraw.elements.twoterm.PotentiometerIEC")

schemdraw.elements.twoterm.Potentiometer[¶](#schemdraw.elements.twoterm.Potentiometer "Link to this definition")

alias of [`PotentiometerIEEE`](#schemdraw.elements.twoterm.PotentiometerIEEE "schemdraw.elements.twoterm.PotentiometerIEEE")

_class_ schemdraw.elements.twoterm.PotentiometerIEC(_\*d_, _\*\*kwargs_)[¶](#schemdraw.elements.twoterm.PotentiometerIEC "Link to this definition")

Potentiometer (European style)

Anchors:

tap

_class_ schemdraw.elements.twoterm.PotentiometerIEEE(_\*d_, _\*\*kwargs_)[¶](#schemdraw.elements.twoterm.PotentiometerIEEE "Link to this definition")

Potentiometer (U.S. style)

Anchors:

tap

schemdraw.elements.twoterm.RBox[¶](#schemdraw.elements.twoterm.RBox "Link to this definition")

alias of [`ResistorIEC`](#schemdraw.elements.twoterm.ResistorIEC "schemdraw.elements.twoterm.ResistorIEC")

schemdraw.elements.twoterm.RBoxVar[¶](#schemdraw.elements.twoterm.RBoxVar "Link to this definition")

alias of [`ResistorVarIEC`](#schemdraw.elements.twoterm.ResistorVarIEC "schemdraw.elements.twoterm.ResistorVarIEC")

schemdraw.elements.twoterm.Resistor[¶](#schemdraw.elements.twoterm.Resistor "Link to this definition")

alias of [`ResistorIEEE`](#schemdraw.elements.twoterm.ResistorIEEE "schemdraw.elements.twoterm.ResistorIEEE")

_class_ schemdraw.elements.twoterm.ResistorIEC(_\*d_, _\*\*kwargs_)[¶](#schemdraw.elements.twoterm.ResistorIEC "Link to this definition")

Resistor as box (IEC/European style)

_class_ schemdraw.elements.twoterm.ResistorIEEE(_\*d_, _\*\*kwargs_)[¶](#schemdraw.elements.twoterm.ResistorIEEE "Link to this definition")

Resistor (IEEE/U.S. style)

schemdraw.elements.twoterm.ResistorVar[¶](#schemdraw.elements.twoterm.ResistorVar "Link to this definition")

alias of [`ResistorVarIEEE`](#schemdraw.elements.twoterm.ResistorVarIEEE "schemdraw.elements.twoterm.ResistorVarIEEE")

_class_ schemdraw.elements.twoterm.ResistorVarIEC(_\*d_, _\*\*kwargs_)[¶](#schemdraw.elements.twoterm.ResistorVarIEC "Link to this definition")

Variable resistor (European style)

_class_ schemdraw.elements.twoterm.ResistorVarIEEE(_\*d_, _\*\*kwargs_)[¶](#schemdraw.elements.twoterm.ResistorVarIEEE "Link to this definition")

Variable resistor (U.S. style)

_class_ schemdraw.elements.twoterm.Rshunt(_\*d_, _\*\*kwargs_)[¶](#schemdraw.elements.twoterm.Rshunt "Link to this definition")

Shunt Resistor

_class_ schemdraw.elements.twoterm.SCR(_\*d_, _\*\*kwargs_)[¶](#schemdraw.elements.twoterm.SCR "Link to this definition")

Silicon controlled rectifier (or thyristor)

Anchors:

gate

_class_ schemdraw.elements.twoterm.Schottky(_\*d_, _\*\*kwargs_)[¶](#schemdraw.elements.twoterm.Schottky "Link to this definition")

Schottky Diode

_class_ schemdraw.elements.twoterm.SparkGap(_\*d_, _\*\*kwargs_)[¶](#schemdraw.elements.twoterm.SparkGap "Link to this definition")

Spark Gap

_class_ schemdraw.elements.twoterm.Thermistor(_\*d_, _\*\*kwargs_)[¶](#schemdraw.elements.twoterm.Thermistor "Link to this definition")

_class_ schemdraw.elements.twoterm.Triac(_\*d_, _\*\*kwargs_)[¶](#schemdraw.elements.twoterm.Triac "Link to this definition")

Anchors:

gate

_class_ schemdraw.elements.twoterm.Varactor(_\*d_, _\*\*kwargs_)[¶](#schemdraw.elements.twoterm.Varactor "Link to this definition")

Varactor Diode/Varicap/Variable Capacitance Diode

_class_ schemdraw.elements.twoterm.VoltageMirror(_\*d_, _\*\*kwargs_)[¶](#schemdraw.elements.twoterm.VoltageMirror "Link to this definition")

Voltage mirror with optional common terminal

This element does not support filling

Anchors:

*   scommon
    

_class_ schemdraw.elements.twoterm.Zener(_\*d_, _\*\*kwargs_)[¶](#schemdraw.elements.twoterm.Zener "Link to this definition")

Zener Diode

Sources, meters, and lamp elements

_class_ schemdraw.elements.sources.Battery(_\*d_, _\*\*kwargs_)[¶](#schemdraw.elements.sources.Battery "Link to this definition")

_class_ schemdraw.elements.sources.BatteryCell(_\*d_, _\*\*kwargs_)[¶](#schemdraw.elements.sources.BatteryCell "Link to this definition")

Cell

_class_ schemdraw.elements.sources.Lamp(_\*d_, _\*\*kwargs_)[¶](#schemdraw.elements.sources.Lamp "Link to this definition")

Incandescent Lamp

_class_ schemdraw.elements.sources.MeterA(_\*d_, _\*\*kwargs_)[¶](#schemdraw.elements.sources.MeterA "Link to this definition")

Ammeter

_class_ schemdraw.elements.sources.MeterI(_\*d_, _\*\*kwargs_)[¶](#schemdraw.elements.sources.MeterI "Link to this definition")

Current Meter (I)

_class_ schemdraw.elements.sources.MeterOhm(_\*d_, _\*\*kwargs_)[¶](#schemdraw.elements.sources.MeterOhm "Link to this definition")

Ohm meter

_class_ schemdraw.elements.sources.MeterV(_\*d_, _\*\*kwargs_)[¶](#schemdraw.elements.sources.MeterV "Link to this definition")

Volt meter

_class_ schemdraw.elements.sources.Neon(_\*d_, _\*\*kwargs_)[¶](#schemdraw.elements.sources.Neon "Link to this definition")

Neon bulb

_class_ schemdraw.elements.sources.Solar(_\*d_, _\*\*kwargs_)[¶](#schemdraw.elements.sources.Solar "Link to this definition")

Solar source

_class_ schemdraw.elements.sources.Source(_\*d_, _\*\*kwargs_)[¶](#schemdraw.elements.sources.Source "Link to this definition")

Generic source element

_class_ schemdraw.elements.sources.SourceControlled(_\*d_, _\*\*kwargs_)[¶](#schemdraw.elements.sources.SourceControlled "Link to this definition")

Generic controlled source

_class_ schemdraw.elements.sources.SourceControlledI(_\*d_, _\*\*kwargs_)[¶](#schemdraw.elements.sources.SourceControlledI "Link to this definition")

Controlled current source

_class_ schemdraw.elements.sources.SourceControlledV(_\*d_, _\*\*kwargs_)[¶](#schemdraw.elements.sources.SourceControlledV "Link to this definition")

Controlled voltage source

_class_ schemdraw.elements.sources.SourceI(_\*d_, _\*\*kwargs_)[¶](#schemdraw.elements.sources.SourceI "Link to this definition")

Current source

_class_ schemdraw.elements.sources.SourcePulse(_\*d_, _\*\*kwargs_)[¶](#schemdraw.elements.sources.SourcePulse "Link to this definition")

Pulse source

_class_ schemdraw.elements.sources.SourceRamp(_\*d_, _\*\*kwargs_)[¶](#schemdraw.elements.sources.SourceRamp "Link to this definition")

Ramp/sawtooth source

_class_ schemdraw.elements.sources.SourceSin(_\*d_, _\*\*kwargs_)[¶](#schemdraw.elements.sources.SourceSin "Link to this definition")

Source with sine

_class_ schemdraw.elements.sources.SourceSquare(_\*d_, _\*\*kwargs_)[¶](#schemdraw.elements.sources.SourceSquare "Link to this definition")

Square wave source

_class_ schemdraw.elements.sources.SourceTriangle(_\*d_, _\*\*kwargs_)[¶](#schemdraw.elements.sources.SourceTriangle "Link to this definition")

Triangle source

_class_ schemdraw.elements.sources.SourceV(_\*d_, _\*\*kwargs_)[¶](#schemdraw.elements.sources.SourceV "Link to this definition")

Voltage source

#### One-terminal Elements[¶](#module-schemdraw.elements.oneterm "Link to this heading")

One terminal element definitions

_class_ schemdraw.elements.oneterm.Antenna(_\*d_, _\*\*kwargs_)[¶](#schemdraw.elements.oneterm.Antenna "Link to this definition")

_class_ schemdraw.elements.oneterm.AntennaLoop(_\*d_, _\*\*kwargs_)[¶](#schemdraw.elements.oneterm.AntennaLoop "Link to this definition")

Loop antenna (diamond style)

_class_ schemdraw.elements.oneterm.AntennaLoop2(_\*d_, _\*\*kwargs_)[¶](#schemdraw.elements.oneterm.AntennaLoop2 "Link to this definition")

Loop antenna (square style)

_class_ schemdraw.elements.oneterm.Ground(_\*d_, _lead: bool \= True_, _\*\*kwargs_)[¶](#schemdraw.elements.oneterm.Ground "Link to this definition")

Ground connection

_class_ schemdraw.elements.oneterm.GroundChassis(_\*d_, _lead: bool \= True_, _\*\*kwargs_)[¶](#schemdraw.elements.oneterm.GroundChassis "Link to this definition")

Chassis ground

_class_ schemdraw.elements.oneterm.GroundSignal(_\*d_, _lead: bool \= True_, _\*\*kwargs_)[¶](#schemdraw.elements.oneterm.GroundSignal "Link to this definition")

Signal ground

_class_ schemdraw.elements.oneterm.NoConnect(_\*\*kwargs_)[¶](#schemdraw.elements.oneterm.NoConnect "Link to this definition")

No Connection

_class_ schemdraw.elements.oneterm.Vdd(_\*d_, _lead: bool \= True_, _\*\*kwargs_)[¶](#schemdraw.elements.oneterm.Vdd "Link to this definition")

Vdd connection

_class_ schemdraw.elements.oneterm.Vss(_\*d_, _lead: bool \= True_, _\*\*kwargs_)[¶](#schemdraw.elements.oneterm.Vss "Link to this definition")

Vss connection

#### Switches[¶](#module-schemdraw.elements.switches "Link to this heading")

Switches and buttons

_class_ schemdraw.elements.switches.Button(_\*d_, _nc: bool \= False_, _\*\*kwargs_)[¶](#schemdraw.elements.switches.Button "Link to this definition")

Push button switch

Parameters:

**nc** – Normally closed

_class_ schemdraw.elements.switches.Switch(_\*d_, _action: Literal\['open', 'close'\] | None \= None_, _\*\*kwargs_)[¶](#schemdraw.elements.switches.Switch "Link to this definition")

Toggle Switch

Parameters:

**action** – action arrow (‘open’ or ‘close’)

_class_ schemdraw.elements.switches.SwitchDIP(_\*d_, _n: int \= 3_, _pattern: Sequence\[bool\] \= None_, _switchcolor: str \= '#333333'_, _swidth: float \= 0.4_, _spacing: float \= 0.2_, _\*\*kwargs_)[¶](#schemdraw.elements.switches.SwitchDIP "Link to this definition")

DIP switch

Parameters:

*   **n** – Number of switches
    
*   **pattern** – Boolean sequence indicating whether each switch is flipped up or down
    
*   **switchcolor** – Fill color for flipped switches
    
*   **swidth** – Width of one switch
    
*   **spacing** – Spacing between switches
    

_class_ schemdraw.elements.switches.SwitchDpdt(_\*d_, _link: bool \= True_, _\*\*kwargs_)[¶](#schemdraw.elements.switches.SwitchDpdt "Link to this definition")

Double-pole double-throw switch

Parameters:

**link** – Show dotted line linking switch levers

Anchors:

*   p1
    
*   p2
    
*   t1
    
*   t2
    
*   t3
    
*   t4
    

_class_ schemdraw.elements.switches.SwitchDpst(_\*d_, _link: bool \= True_, _\*\*kwargs_)[¶](#schemdraw.elements.switches.SwitchDpst "Link to this definition")

Double-pole single-throw switch

Parameters:

**link** – Show dotted line linking switch levers

Anchors:

*   p1
    
*   p2
    
*   t1
    
*   t2
    

_class_ schemdraw.elements.switches.SwitchReed(_\*d_, _\*\*kwargs_)[¶](#schemdraw.elements.switches.SwitchReed "Link to this definition")

Reed Switch

_class_ schemdraw.elements.switches.SwitchRotary(_\*d_, _n: int \= 4_, _dtheta: float \= None_, _theta0: float \= None_, _radius: float \= 1_, _arrowlen: float \= 0.75_, _arrowcontact: int \= 0_, _\*\*kwargs_)[¶](#schemdraw.elements.switches.SwitchRotary "Link to this definition")

Rotary Switch

Parameters:

*   **n** – number of contacts
    
*   **dtheta** – angle in degrees between each contact
    
*   **theta0** – angle in degrees of first contact
    
*   **radius** – radius of switch
    
*   **arrowlen** – length of switch arrow
    
*   **arrowcontact** – index of contact to point to
    

Values for dtheta and theta will be calculated based on n if not provided.

Anchors:

*   P
    
*   T\[x\] for each contact (starting at 1)
    

_class_ schemdraw.elements.switches.SwitchSpdt(_\*d_, _action: Literal\['open', 'close'\] | None \= None_, _\*\*kwargs_)[¶](#schemdraw.elements.switches.SwitchSpdt "Link to this definition")

Single-pole double throw switch.

Parameters:

**action** – action arrow (‘open’ or ‘close’)

Anchors:

*   a
    
*   b
    
*   c
    

_class_ schemdraw.elements.switches.SwitchSpdt2(_\*d_, _action: Literal\['open', 'close'\] | None \= None_, _\*\*kwargs_)[¶](#schemdraw.elements.switches.SwitchSpdt2 "Link to this definition")

Single-pole double throw switch, throws above and below.

Parameters:

**action** – action arrow (‘open’ or ‘close’)

Anchors:

*   a
    
*   b
    
*   c
    

#### Lines[¶](#module-schemdraw.elements.lines "Link to this heading")

Lines, Arrows, and Labels

_class_ schemdraw.elements.lines.Annotate(_k\=0.75_, _th1\=75_, _th2\=180_, _arrow\='<-'_, _arrowlength\=0.25_, _arrowwidth\=0.2_, _\*\*kwargs_)[¶](#schemdraw.elements.lines.Annotate "Link to this definition")

Draw a curved arrow pointing to at position, ending at to position, with label location at the tail of the arrow (See also Arc3).

Parameters:

*   **k** – Control point factor. Higher k means tighter curve.
    
*   **th1** – Angle at which the arc leaves start point
    
*   **th2** – Angle at which the arc leaves end point
    
*   **arrow** – arrowhead specifier, such as ‘->’, ‘<-’, ‘<->’, or ‘-o’
    
*   **arrowlength** – Length of arrowhead
    
*   **arrowwidth** – Width of arrowhead
    

_class_ schemdraw.elements.lines.Arc2(_k\=0.5_, _arrow\=None_, _\*\*kwargs_)[¶](#schemdraw.elements.lines.Arc2 "Link to this definition")

Arc Element

Use at and to methods to define endpoints.

Arc2 is a quadratic Bezier curve with control point halfway between the endpoints, generating a symmetric ‘C’ curve.

Parameters:

**k** – Control point factor. Higher k means more curvature.

Anchors:

start end ctrl mid

delta(_dx: float \= 0_, _dy: float \= 0_) → [Element](index.html#schemdraw.elements.Element "schemdraw.elements.elements.Element")[¶](#schemdraw.elements.lines.Arc2.delta "Link to this definition")

Specify change in position

to(_xy: Tuple\[float, float\] | Point_, _dx: float \= 0_, _dy: float \= 0_) → [Element](index.html#schemdraw.elements.Element "schemdraw.elements.elements.Element")[¶](#schemdraw.elements.lines.Arc2.to "Link to this definition")

Specify ending position

Parameters:

*   **xy** – Ending position of element
    
*   **dx** – X-offset from xy position
    
*   **dy** – Y-offset from xy position
    

_class_ schemdraw.elements.lines.Arc3(_k\=0.75_, _th1\=0_, _th2\=180_, _arrow\=None_, _arrowlength\=0.25_, _arrowwidth\=0.2_, _\*\*kwargs_)[¶](#schemdraw.elements.lines.Arc3 "Link to this definition")

Arc Element

Use at and to methods to define endpoints.

Arc3 is a cubic Bezier curve. Control points are set to extend the curve at the given angle for each endpoint.

Parameters:

*   **k** – Control point factor. Higher k means tighter curve.
    
*   **th1** – Angle at which the arc leaves start point
    
*   **th2** – Angle at which the arc leaves end point
    
*   **arrow** – arrowhead specifier, such as ‘->’, ‘<-’, ‘<->’, or ‘-o’
    
*   **arrowlength** – Length of arrowhead
    
*   **arrowwidth** – Width of arrowhead
    

Anchors:

start end center ctrl1 ctrl2

delta(_dx: float \= 0_, _dy: float \= 0_) → [Element](index.html#schemdraw.elements.Element "schemdraw.elements.elements.Element")[¶](#schemdraw.elements.lines.Arc3.delta "Link to this definition")

Specify change in position

to(_xy: Tuple\[float, float\] | Point_, _dx: float \= 0_, _dy: float \= 0_) → [Element](index.html#schemdraw.elements.Element "schemdraw.elements.elements.Element")[¶](#schemdraw.elements.lines.Arc3.to "Link to this definition")

Specify ending position

Parameters:

*   **xy** – Ending position of element
    
*   **dx** – X-offset from xy position
    
*   **dy** – Y-offset from xy position
    

_class_ schemdraw.elements.lines.ArcLoop(_radius: float \= 0.6_, _arrow: str \= None_, _arrowlength\=0.25_, _arrowwidth\=0.2_, _\*\*kwargs_)[¶](#schemdraw.elements.lines.ArcLoop "Link to this definition")

Loop Arc

Use at and to methods to define endpoints.

ArcLoop is an arc drawn as part of a circle.

Parameters:

*   **radius** – Radius of the arc
    
*   **arrow** – arrowhead specifier, such as ‘->’, ‘<-’, ‘<->’, or ‘-o’ arrowlength: Length of arrowhead
    
*   **arrowwidth** – Width of arrowhead
    

Anchors:

start end mid BL BR TL TR

delta(_dx: float \= 0_, _dy: float \= 0_)[¶](#schemdraw.elements.lines.ArcLoop.delta "Link to this definition")

Specify ending position relative to start position

to(_xy: Tuple\[float, float\] | Point_, _dx: float \= 0_, _dy: float \= 0_) → [Element](index.html#schemdraw.elements.Element "schemdraw.elements.elements.Element")[¶](#schemdraw.elements.lines.ArcLoop.to "Link to this definition")

Specify ending position

Parameters:

*   **xy** – Ending position of element
    
*   **dx** – X-offset from xy position
    
*   **dy** – Y-offset from xy position
    

_class_ schemdraw.elements.lines.ArcN(_k\=0.75_, _arrow\=None_, _arrowlength\=0.25_, _arrowwidth\=0.2_, _\*\*kwargs_)[¶](#schemdraw.elements.lines.ArcN "Link to this definition")

N-Curve Arc

Use at and to methods to define endpoints.

ArcN approaches the endpoints vertically, leading to a ‘N’ shaped curve

Parameters:

*   **k** – Control point factor. Higher k means tighter curve.
    
*   **arrow** – arrowhead specifier, such as ‘->’, ‘<-’, ‘<->’, or ‘-o’ arrowlength: Length of arrowhead
    
*   **arrowwidth** – Width of arrowhead
    

_class_ schemdraw.elements.lines.ArcZ(_k\=0.75_, _arrow\=None_, _arrowlength\=0.25_, _arrowwidth\=0.2_, _\*\*kwargs_)[¶](#schemdraw.elements.lines.ArcZ "Link to this definition")

Z-Curve Arc

Use at and to methods to define endpoints.

ArcZ approaches the endpoints horizontally, leading to a ‘Z’ shaped curve

Parameters:

*   **k** – Control point factor. Higher k means tighter curve.
    
*   **arrow** – arrowhead specifier, such as ‘->’, ‘<-’, ‘<->’, or ‘-o’ arrowlength: Length of arrowhead
    
*   **arrowwidth** – Width of arrowhead
    

_class_ schemdraw.elements.lines.Arrow(_\*d_, _double: bool \= False_, _headwidth: float \= 0.15_, _headlength: float \= 0.25_, _\*\*kwargs_)[¶](#schemdraw.elements.lines.Arrow "Link to this definition")

Parameters:

*   **double** – Show arrowhead on both ends
    
*   **headwidth** – Width of arrow head
    
*   **headlength** – Length of arrow head
    

_class_ schemdraw.elements.lines.Arrowhead(_\*d_, _headwidth: float \= 0.15_, _headlength: float \= 0.25_, _\*\*kwargs_)[¶](#schemdraw.elements.lines.Arrowhead "Link to this definition")

_class_ schemdraw.elements.lines.CurrentLabel(_ofst: float \= 0.4_, _length: float \= 2_, _top: bool \= True_, _reverse: bool \= False_, _headlength: float \= 0.3_, _headwidth: float \= 0.2_, _\*\*kwargs_)[¶](#schemdraw.elements.lines.CurrentLabel "Link to this definition")

Current label arrow drawn above an element

Use .at() method to place the label over an existing element.

Parameters:

*   **ofst** – Offset distance from centerline of element
    
*   **length** – Length of the arrow
    
*   **top** – Draw arrow on top or bottom of element
    
*   **reverse** – Reverse the arrow direction
    
*   **headlength** – Length of arrowhead
    
*   **headwidth** – Width of arrowhead
    

at(_xy: Tuple\[float, float\] | Point | [Element](index.html#schemdraw.elements.Element "schemdraw.elements.elements.Element")_) → [Element](index.html#schemdraw.elements.Element "schemdraw.elements.elements.Element")[¶](#schemdraw.elements.lines.CurrentLabel.at "Link to this definition")

Specify CurrentLabel position.

If xy is an Element, arrow will be centered along element and its color will also be inherited.

Parameters:

*   **xy** – The absolute (x, y) position or an
    
*   **over** (_Element instance to center the arrow_) –
    

_class_ schemdraw.elements.lines.CurrentLabelInline(_direction: Literal\['in', 'out'\] \= 'in'_, _ofst: float \= 0.8_, _start: bool \= True_, _headlength: float \= 0.3_, _headwidth: float \= 0.3_, _\*\*kwargs_)[¶](#schemdraw.elements.lines.CurrentLabelInline "Link to this definition")

Current direction arrow, inline with element.

Use .at() method to place arrow on an Element instance

Parameters:

*   **direction** – arrow direction ‘in’ or ‘out’ of element
    
*   **ofst** – Offset along lead length
    
*   **start** – Arrow at start or end of element
    
*   **headlength** – Length of arrowhead
    
*   **headwidth** – Width of arrowhead
    

at(_xy: Tuple\[float, float\] | Point | [Element](index.html#schemdraw.elements.Element "schemdraw.elements.elements.Element")_) → [Element](index.html#schemdraw.elements.Element "schemdraw.elements.elements.Element")[¶](#schemdraw.elements.lines.CurrentLabelInline.at "Link to this definition")

Specify CurrentLabelInline position.

If xy is an Element, arrow will be placed along the element’s leads and the arrow color will be inherited.

Parameters:

*   **xy** – The absolute (x, y) position or an
    
*   **on** (_Element instance to place the arrow_) –
    

_class_ schemdraw.elements.lines.DataBusLine(_\*d_, _\*\*kwargs_)[¶](#schemdraw.elements.lines.DataBusLine "Link to this definition")

Straight Line with bus indication stripe

_class_ schemdraw.elements.lines.Dot(_\*d_, _radius: float \= 0.075_, _open: bool \= False_, _\*\*kwargs_)[¶](#schemdraw.elements.lines.Dot "Link to this definition")

Connection Dot

Parameters:

*   **radius** – Radius of dot
    
*   **open** – Draw as an open circle
    

_class_ schemdraw.elements.lines.DotDotDot(_\*d_, _radius: float \= 0.075_, _open: bool \= False_, _\*\*kwargs_)[¶](#schemdraw.elements.lines.DotDotDot "Link to this definition")

Ellipsis element

Parameters:

*   **radius** – Radius of dots
    
*   **open** – Draw dots as open circles
    

“Ellipsis” is a reserved keyword in Python used for slicing, thus the name DotDotDot.

_class_ schemdraw.elements.lines.Encircle(_elm\_list: Sequence\[[Element](index.html#schemdraw.elements.Element "schemdraw.elements.elements.Element")\] \= None_, _padx: float \= 0.2_, _pady: float \= 0.2_, _includelabels: bool \= True_, _\*\*kwargs_)[¶](#schemdraw.elements.lines.Encircle "Link to this definition")

Draw ellipse around all elements in the list

Parameters:

*   **elm\_list** – List of elements to enclose
    
*   **padx** – Horizontal distance from elements to loop
    
*   **pady** – Vertical distance from elements to loop
    
*   **includelabels** – Include labesl in the ellipse
    

_class_ schemdraw.elements.lines.EncircleBox(_elm\_list: Sequence\[[Element](index.html#schemdraw.elements.Element "schemdraw.elements.elements.Element")\] \= None_, _cornerradius: float \= 0.3_, _padx: float \= 0.2_, _pady: float \= 0.2_, _includelabels: bool \= True_, _\*\*kwargs_)[¶](#schemdraw.elements.lines.EncircleBox "Link to this definition")

Draw rounded box around all elements in the list

Parameters:

*   **elm\_list** – List elements to enclose
    
*   **cornerraidus** – radius of corner rounding
    
*   **padx** – Horizontal distance from elements to loop
    
*   **pady** – Vertical distance from elements to loop
    
*   **includelabels** – Include labels in the box
    

_class_ schemdraw.elements.lines.Gap(_\*d_, _\*\*kwargs_)[¶](#schemdraw.elements.lines.Gap "Link to this definition")

Gap for labeling port voltages, for example. Draws nothing, but provides place to attach a label such as (‘+’, ‘V’, ‘-‘).

_class_ schemdraw.elements.lines.Label(_\*d_, _label: str \= None_, _\*\*kwargs_)[¶](#schemdraw.elements.lines.Label "Link to this definition")

Label element.

For more options, use Label().label() method.

Parameters:

**label** – text to display.

_class_ schemdraw.elements.lines.Line(_\*d_, _arrow: str \= None_, _\*\*kwargs_)[¶](#schemdraw.elements.lines.Line "Link to this definition")

Straight Line

Parameters:

**arrow** – arrowhead specifier, such as ‘->’, ‘<-’, ‘<->’, ‘-o’, or ‘|->’

_class_ schemdraw.elements.lines.LoopArrow(_direction: Literal\['cw', 'ccw'\] \= 'cw'_, _theta1: float \= 35_, _theta2: float \= \-35_, _width: float \= 1.0_, _height: float \= 1.0_, _\*\*kwargs_)[¶](#schemdraw.elements.lines.LoopArrow "Link to this definition")

Loop arrow, for mesh analysis notation

Parameters:

*   **direction** – loop direction ‘cw’ or ‘ccw’
    
*   **theta1** – Angle of start of loop arrow
    
*   **theta2** – Angle of end of loop arrow
    
*   **width** – Width of loop
    
*   **height** – Height of loop
    

_class_ schemdraw.elements.lines.LoopCurrent(_elm\_list: Sequence\[[Element](index.html#schemdraw.elements.Element "schemdraw.elements.elements.Element")\] \= None_, _direction: Literal\['cw', 'ccw'\] \= 'cw'_, _theta1: float \= 35_, _theta2: float \= \-35_, _pad: float \= 0.2_, _\*\*kwargs_)[¶](#schemdraw.elements.lines.LoopCurrent "Link to this definition")

Loop current label, for mesh analysis notation, placed within a box of 4 existing elements.

Parameters:

*   **elm\_list** – List of 4 elements surrounding loop, in order (top, right, bottom, left)
    
*   **direction** – loop direction ‘cw’ or ‘ccw’
    
*   **theta1** – Angle of start of loop arrow
    
*   **theta2** – Angle of end of loop arrow
    
*   **pad** – Distance from elements to loop
    

_class_ schemdraw.elements.lines.Rect(_\*d_, _corner1: Tuple\[float, float\] | Point \= (0, 0)_, _corner2: Tuple\[float, float\] | Point \= (1, 1)_, _fill: str \= None_, _lw: float \= None_, _ls: Literal\['-', ':', '--', '-.'\] \= None_, _\*\*kwargs_)[¶](#schemdraw.elements.lines.Rect "Link to this definition")

Rectangle Element

Used mainly for buliding more complex elements. Corner arguments are relative to Element coordinates, not Drawing coordinates.

Parameters:

*   **corner1** – Position of top-left corner
    
*   **corner2** – Position of bottom-right corner
    
*   **fill** – Color to fill if not None
    
*   **lw** – Line width
    
*   **ls** – Line style ‘-’, ‘–’, ‘:’, etc.
    

_class_ schemdraw.elements.lines.Tag(_\*d_, _width: float \= 1.5_, _height: float \= 0.625_, _\*\*kwargs_)[¶](#schemdraw.elements.lines.Tag "Link to this definition")

Tag/flag element for labeling signal names.

Because text size is unknown until drawn, must specify width manually to fit a given text label.

Parameters:

*   **width** – Width of the tag
    
*   **height** – Height of the tag
    

_class_ schemdraw.elements.lines.Wire(_shape: str \= '-'_, _k: float \= 1_, _arrow: str \= None_, _\*\*kwargs_)[¶](#schemdraw.elements.lines.Wire "Link to this definition")

Connect the .at() and .to() positions with lines depending on shape

Parameters:

*   **shape** – Determines shape of wire: \-: straight line |-: right-angle line starting vertically \-|: right-angle line starting horizontally ‘z’: diagonal line with horizontal end segments ‘N’: diagonal line with vertical end segments n: n- or u-shaped lines c: c- or ↄ-shaped lines
    
*   **k** – Distance before the wire changes directions in n and c shapes.
    
*   **arrow** – arrowhead specifier, such as ‘->’, ‘<-’, ‘<->’, or ‘-o’
    

delta(_dx: float \= 0_, _dy: float \= 0_)[¶](#schemdraw.elements.lines.Wire.delta "Link to this definition")

Specify ending position relative to start position

dot(_open: bool \= False_) → [Element](index.html#schemdraw.elements.Element "schemdraw.elements.elements.Element")[¶](#schemdraw.elements.lines.Wire.dot "Link to this definition")

Add a dot to the end of the element

idot(_open: bool \= False_) → [Element](index.html#schemdraw.elements.Element "schemdraw.elements.elements.Element")[¶](#schemdraw.elements.lines.Wire.idot "Link to this definition")

Add a dot to the input/start of the element

to(_xy: Tuple\[float, float\] | Point_, _dx: float \= 0_, _dy: float \= 0_) → [Element](index.html#schemdraw.elements.Element "schemdraw.elements.elements.Element")[¶](#schemdraw.elements.lines.Wire.to "Link to this definition")

Specify ending position

Parameters:

*   **xy** – Ending position of element
    
*   **dx** – X-offset from xy position
    
*   **dy** – Y-offset from xy position
    

_class_ schemdraw.elements.lines.ZLabel(_ofst: float \= 0.5_, _hofst: float \= 0.4_, _length: float \= 1_, _lengthtip: float \= 0.5_, _headlength: float \= 0.25_, _headwidth: float \= 0.15_, _\*\*kwargs_)[¶](#schemdraw.elements.lines.ZLabel "Link to this definition")

Right-angle arrow, often used to indicate impedance looking in to a node

Use .at() method to place the label over an existing element.

Parameters:

*   **ofst** – Vertical offset from centerline of element
    
*   **hofst** – Horizontal offset from center of element
    
*   **length** – Length of the arrow tail
    
*   **lengthtip** – Length of the arrow tip
    
*   **headlength** – Arrowhead length
    
*   **headwidth** – Arrowhead width
    

at(_xy: Tuple\[float, float\] | Point | [Element](index.html#schemdraw.elements.Element "schemdraw.elements.elements.Element")_) → [Element](index.html#schemdraw.elements.Element "schemdraw.elements.elements.Element")[¶](#schemdraw.elements.lines.ZLabel.at "Link to this definition")

Specify CurrentLabel position.

If xy is an Element, arrow will be centered along element and its color will also be inherited.

Parameters:

*   **xy** – The absolute (x, y) position or an
    
*   **over** (_Element instance to center the arrow_) –
    

#### Cables and Connectors[¶](#module-schemdraw.elements.cables "Link to this heading")

Cable elements, coaxial and triaxial

_class_ schemdraw.elements.cables.Coax(_\*d_, _length: float \= 3_, _radius: float \= 0.3_, _leadlen: float \= 0.6_, _\*\*kwargs_)[¶](#schemdraw.elements.cables.Coax "Link to this definition")

Coaxial cable element.

Parameters:

*   **length** – Total length of the cable, excluding lead extensions.
    
*   **radius** – Radius of shield
    
*   **leadlen** – Distance (x) from start of center conductor to start of shield.
    

Anchors:

*   shieldstart
    
*   shieldstart\_top
    
*   shieldend
    
*   shieldend\_top
    
*   shieldcenter
    
*   shieldcenter\_top
    

_class_ schemdraw.elements.cables.Triax(_\*d_, _length: float \= 3_, _leadlen: float \= 0.6_, _radiusinner: float \= 0.3_, _radiusouter: float \= 0.6_, _shieldofststart: float \= 0.3_, _shieldofstend: float \= 0.3_, _\*\*kwargs_)[¶](#schemdraw.elements.cables.Triax "Link to this definition")

Triaxial cable element.

Parameters:

*   **length** – Total length of the cable
    
*   **radiusinner** – Radius of inner guard
    
*   **radiusouter** – Radius of outer shield
    
*   **leadlen** – Distance (x) from start of center conductor to start of guard.
    
*   **shieldofststart** – Distance from start of inner guard to start of outer shield
    
*   **shieldofstend** – Distance from end of outer shield to end of inner guard
    

Anchors:

*   shieldstart
    
*   shieldstart\_top
    
*   shieldend
    
*   shieldend\_top
    
*   shieldcenter
    
*   shieldcenter\_top
    
*   guardstart
    
*   guardstart\_top
    
*   guardend
    
*   guardend\_top
    

Connectors and bus lines

_class_ schemdraw.elements.connectors.BusConnect(_\*d_, _n: int \= 1_, _dy: float \= 0.6_, _up: bool \= True_, _lwbus: float \= 4_, _l: float \= 3_, _\*\*kwargs_)[¶](#schemdraw.elements.connectors.BusConnect "Link to this definition")

Data bus connection.

Adds the short diagonal lines that break out a bus (wide line) to connect to an Ic or Header element.

Parameters:

*   **n** – Number of parallel lines
    
*   **dy** – Distance between parallel lines
    
*   **up** – Slant up or down
    
*   **lwbus** – Line width of bus line
    
*   **l** – length of connection lines
    

Anchors:

*   start
    
*   end
    
*   p\[X\] where X is int for each data line
    

_class_ schemdraw.elements.connectors.BusLine(_\*d_, _lw: float \= 4_, _\*\*kwargs_)[¶](#schemdraw.elements.connectors.BusLine "Link to this definition")

Data bus line. Just a wide line.

Use BusConnect to break out connections to the BusLine.

Parameters:

**lw** – Line width

_class_ schemdraw.elements.connectors.CoaxConnect(_\*d_, _radius: float \= 0.4_, _radiusinner: float \= 0.12_, _fillinner: str \= 'bg'_, _\*\*kwargs_)[¶](#schemdraw.elements.connectors.CoaxConnect "Link to this definition")

Coaxial connector

Parameters:

*   **radius** – Radius of outer shell
    
*   **radiusinner** – Radius of inner conductor
    
*   **fillinner** – Color to fill inner conductor
    

Anchors:

*   center
    
*   N
    
*   S
    
*   E
    
*   W
    

_class_ schemdraw.elements.connectors.DB25(_\*d_, _pinspacing: float \= 0.6_, _edge: float \= 0.3_, _number: bool \= False_, _pinfill: str \= 'bg'_, _\*\*kwargs_)[¶](#schemdraw.elements.connectors.DB25 "Link to this definition")

DB25 Connector

Parameters:

*   **pinspacing** – Distance between pins
    
*   **edge** – Distance between edge and pins
    
*   **number** – Draw pin numbers
    
*   **pinfill** – Color to fill pin circles
    

Anchors:

*   pin1 thru pin25
    

_class_ schemdraw.elements.connectors.DB9(_\*d_, _pinspacing: float \= 0.6_, _edge: float \= 0.3_, _number: bool \= False_, _pinfill: str \= 'bg'_, _\*\*kwargs_)[¶](#schemdraw.elements.connectors.DB9 "Link to this definition")

DB9 Connector

Parameters:

*   **pinspacing** – Distance between pins
    
*   **edge** – Distance between edge and pins
    
*   **number** – Draw pin numbers
    
*   **pinfill** – Color to fill pin circles
    

Anchors:

*   pin1 thru pin9
    

_class_ schemdraw.elements.connectors.Header(_\*d_, _rows: int \= 4_, _cols: int \= 1_, _style: Literal\['round', 'square', 'screw'\] \= 'round'_, _numbering: Literal\['lr', 'ud', 'ccw'\] \= 'lr'_, _shownumber: bool \= False_, _pinsleft: Sequence\[str\] \= None_, _pinsright: Sequence\[str\] \= None_, _pinalignleft: Literal\['center', 'top', 'bottom'\] \= 'bottom'_, _pinalignright: Literal\['center', 'top', 'bottom'\] \= 'bottom'_, _pinfontsizeright: float \= 9_, _pinfontsizeleft: float \= 9_, _pinspacing: float \= 0.6_, _edge: float \= 0.3_, _pinfill: str \= 'bg'_, _\*\*kwargs_)[¶](#schemdraw.elements.connectors.Header "Link to this definition")

Header connector element

Parameters:

*   **rows** – Number of rows
    
*   **cols** – Number of columns. Pin numbering requires 1 or 2 columns
    
*   **style** – Connector style, ‘round’, ‘square’, or ‘screw’
    
*   **numbering** – Pin numbering order. ‘lr’ for left-to-right numbering, ‘ud’ for up-down numbering, or ‘ccw’ for counter-clockwise (integrated-circuit style) numbering. Pin 1 is always at the top-left corner, unless flip method is also called.
    
*   **shownumber** – Draw pin numbers outside the header
    
*   **pinsleft** – List of pin labels for left side
    
*   **pinsright** – List of pin labels for right side
    
*   **pinalignleft** – Vertical alignment for pins on left side (‘center’, ‘top’, ‘bottom’)
    
*   **pinalignright** – Vertical alignment for pins on right side (‘center’, ‘top’, ‘bottom’)
    
*   **pinfontsizeleft** – Font size for pin labels on left
    
*   **pinfontsizeright** – Font size for pin labels on right
    
*   **pinspacing** – Distance between pins
    
*   **edge** – Distance between header edge and first pin row/column
    
*   **pinfill** – Color to fill pin circles
    

Anchors:

pin\[X\] for each pin

_class_ schemdraw.elements.connectors.Jack(_\*d_, _\*\*kwargs_)[¶](#schemdraw.elements.connectors.Jack "Link to this definition")

Jack (female connector)

_class_ schemdraw.elements.connectors.Jumper(_\*d_, _pinspacing: float \= 0.6_, _\*\*kwargs_)[¶](#schemdraw.elements.connectors.Jumper "Link to this definition")

Jumper for use on a Header element

Set position using at() method with a Header pin location, e.g. Jumper().at(H.in1)

Parameters:

**pinspacing** – Spacing between pins

_class_ schemdraw.elements.connectors.OrthoLines(_\*d_, _n: int \= 1_, _dy: float \= 0.6_, _xstart: float \= None_, _arrow: str \= None_, _\*\*kwargs_)[¶](#schemdraw.elements.connectors.OrthoLines "Link to this definition")

Orthogonal multiline connectors

Use at() and to() methods to specify starting and ending location of OrthoLines.

The default lines are spaced to provide connection to pins with default spacing on Ic element or connector such as a Header.

Parameters:

*   **n** – Number of parallel lines
    
*   **dy** – Distance between parallel lines
    
*   **xstart** – Fractional distance (0-1) to start vertical portion of first ortholine
    

delta(_dx: float \= 0_, _dy: float \= 0_)[¶](#schemdraw.elements.connectors.OrthoLines.delta "Link to this definition")

Specify ending position relative to start position

to(_xy: Tuple\[float, float\] | Point_) → [Element](index.html#schemdraw.elements.Element "schemdraw.elements.elements.Element")[¶](#schemdraw.elements.connectors.OrthoLines.to "Link to this definition")

Specify ending position of OrthoLines

_class_ schemdraw.elements.connectors.Plug(_\*d_, _\*\*kwargs_)[¶](#schemdraw.elements.connectors.Plug "Link to this definition")

Plug (male connector)

_class_ schemdraw.elements.connectors.RightLines(_\*d_, _n: int \= 1_, _dy: float \= 0.6_, _arrow: str \= None_, _\*\*kwargs_)[¶](#schemdraw.elements.connectors.RightLines "Link to this definition")

Right-angle multi-line connectors

Use at() and to() methods to specify starting and ending location.

The default lines are spaced to provide connection to pins with default spacing on Ic element or connector such as a Header.

Parameters:

*   **n** – Number of parallel lines
    
*   **dy** – Distance between parallel lines
    

delta(_dx: float \= 0_, _dy: float \= 0_)[¶](#schemdraw.elements.connectors.RightLines.delta "Link to this definition")

Specify ending position relative to start position

to(_xy: Tuple\[float, float\] | Point_) → [Element](index.html#schemdraw.elements.Element "schemdraw.elements.elements.Element")[¶](#schemdraw.elements.connectors.RightLines.to "Link to this definition")

Specify ending position of OrthoLines

#### Transistors[¶](#module-schemdraw.elements.transistors "Link to this heading")

Transistor elements

_class_ schemdraw.elements.transistors.AnalogBiasedFet(_\*d_, _bulk: bool \= False_, _offset\_gate: bool \= True_, _arrow: bool \= True_, _\*\*kwargs_)[¶](#schemdraw.elements.transistors.AnalogBiasedFet "Link to this definition")

Generic biased small-signal Field Effect Transistor, analog style

Parameters:

*   **bulk** – Draw bulk contact
    
*   **offset\_gate** – Draw gate on the source side of the transistor, rather than middle
    
*   **arrow** – Draw source dot on the transistor if bulk dot is not drawn
    

Anchors:

source drain gate bulk (if bulk=True) center

_class_ schemdraw.elements.transistors.AnalogNFet(_\*d_, _bulk: bool \= False_, _offset\_gate: bool \= True_, _arrow: bool \= True_, _\*\*kwargs_)[¶](#schemdraw.elements.transistors.AnalogNFet "Link to this definition")

N-type Field Effect Transistor, analog style

Parameters:

*   **bulk** – Draw bulk contact
    
*   **offset\_gate** – Draw gate on the source side of the transistor, rather than middle
    
*   **arrow** – Draw source arrow on the transistor if bulk arrow is not drawn
    

Anchors:

source drain gate bulk (if bulk=True) center

_class_ schemdraw.elements.transistors.AnalogPFet(_\*d_, _bulk: bool \= False_, _offset\_gate: bool \= True_, _arrow: bool \= True_, _\*\*kwargs_)[¶](#schemdraw.elements.transistors.AnalogPFet "Link to this definition")

P-type Field Effect Transistor, analog style

Parameters:

*   **bulk** – Draw bulk contact
    
*   **offset\_gate** – Draw gate on the source side of the transistor, rather than middle
    
*   **arrow** – Draw source arrow on the transistor if bulk arrow is not drawn
    

Anchors:

source drain gate bulk (if bulk=True) center

_class_ schemdraw.elements.transistors.Bjt(_\*d_, _circle: bool \= False_, _\*\*kwargs_)[¶](#schemdraw.elements.transistors.Bjt "Link to this definition")

Bipolar Junction Transistor (untyped)

Parameters:

**circle** – Draw circle around the transistor

Anchors:

*   collector
    
*   emitter
    
*   base
    
*   center
    

_class_ schemdraw.elements.transistors.Bjt2(_\*d_, _circle: bool \= False_, _\*\*kwargs_)[¶](#schemdraw.elements.transistors.Bjt2 "Link to this definition")

Bipolar Junction Transistor (untyped) which extends collector/emitter leads to the desired length

Parameters:

**circle** – Draw circle around the transistor

Anchors:

*   collector
    
*   emitter
    
*   base
    

_class_ schemdraw.elements.transistors.BjtNpn(_\*d_, _circle: bool \= False_, _\*\*kwargs_)[¶](#schemdraw.elements.transistors.BjtNpn "Link to this definition")

NPN Bipolar Junction Transistor

Parameters:

**circle** – Draw circle around the transistor

Anchors:

*   collector
    
*   emitter
    
*   base
    
*   center
    

_class_ schemdraw.elements.transistors.BjtNpn2(_\*d_, _circle: bool \= False_, _\*\*kwargs_)[¶](#schemdraw.elements.transistors.BjtNpn2 "Link to this definition")

NPN Bipolar Junction Transistor which extends collector/emitter leads to the desired length

Parameters:

**circle** – Draw circle around the transistor

Anchors:

*   collector
    
*   emitter
    
*   base
    

_class_ schemdraw.elements.transistors.BjtPnp(_\*d_, _circle: bool \= False_, _\*\*kwargs_)[¶](#schemdraw.elements.transistors.BjtPnp "Link to this definition")

PNP Bipolar Junction Transistor

Parameters:

**circle** – Draw circle around the transistor

Anchors:

*   collector
    
*   emitter
    
*   base
    
*   center
    

_class_ schemdraw.elements.transistors.BjtPnp2(_\*d_, _circle: bool \= False_, _\*\*kwargs_)[¶](#schemdraw.elements.transistors.BjtPnp2 "Link to this definition")

PNP Bipolar Junction Transistor which extends collector/emitter leads to the desired length

Parameters:

**circle** – Draw circle around the transistor

Anchors:

*   collector
    
*   emitter
    
*   base
    

_class_ schemdraw.elements.transistors.BjtPnp2c(_\*d_, _circle: bool \= False_, _\*\*kwargs_)[¶](#schemdraw.elements.transistors.BjtPnp2c "Link to this definition")

PNP Bipolar Junction Transistor with 2 collectors

Parameters:

**circle** – Draw circle around the transistor

Anchors:

*   collector
    
*   emitter
    
*   base
    
*   C2
    
*   center
    

_class_ schemdraw.elements.transistors.BjtPnp2c2(_\*d_, _circle: bool \= False_, _\*\*kwargs_)[¶](#schemdraw.elements.transistors.BjtPnp2c2 "Link to this definition")

2-Collector PNP Bipolar Junction Transistor which extends collector/emitter leads to the desired length

Parameters:

**circle** – Draw circle around the transistor

Anchors:

*   collector
    
*   emitter
    
*   base
    
*   C2
    

_class_ schemdraw.elements.transistors.JFet(_\*d_, _circle: bool \= False_, _\*\*kwargs_)[¶](#schemdraw.elements.transistors.JFet "Link to this definition")

Junction Field Effect Transistor (untyped)

Anchors:

*   source
    
*   drain
    
*   gate
    
*   center
    

_class_ schemdraw.elements.transistors.JFet2(_\*d_, _circle: bool \= False_, _\*\*kwargs_)[¶](#schemdraw.elements.transistors.JFet2 "Link to this definition")

Junction Field Effect Transistor (untyped) which extends collector/emitter leads to the desired length

Anchors:

*   source
    
*   drain
    
*   gate
    

_class_ schemdraw.elements.transistors.JFetN(_\*d_, _circle: bool \= False_, _\*\*kwargs_)[¶](#schemdraw.elements.transistors.JFetN "Link to this definition")

N-type Junction Field Effect Transistor

Parameters:

**circle** – Draw circle around the transistor

Anchors:

*   source
    
*   drain
    
*   gate
    
*   center
    

_class_ schemdraw.elements.transistors.JFetN2(_\*d_, _circle: bool \= False_, _\*\*kwargs_)[¶](#schemdraw.elements.transistors.JFetN2 "Link to this definition")

N-type Junction Field Effect Transistor which extends collector/emitter leads to the desired length

Parameters:

**circle** – Draw circle around the transistor

Anchors:

*   source
    
*   drain
    
*   gate
    

_class_ schemdraw.elements.transistors.JFetP(_\*d_, _circle: bool \= False_, _\*\*kwargs_)[¶](#schemdraw.elements.transistors.JFetP "Link to this definition")

P-type Junction Field Effect Transistor

Parameters:

**circle** – Draw circle around the transistor

Anchors:

*   source
    
*   drain
    
*   gate
    
*   center
    

_class_ schemdraw.elements.transistors.JFetP2(_\*d_, _circle: bool \= False_, _\*\*kwargs_)[¶](#schemdraw.elements.transistors.JFetP2 "Link to this definition")

P-type Junction Field Effect Transistor which extends collector/emitter leads to the desired length

Parameters:

**circle** – Draw circle around the transistor

Anchors:

*   source
    
*   drain
    
*   gate
    

_class_ schemdraw.elements.transistors.NFet(_\*d_, _bulk: bool \= False_, _\*\*kwargs_)[¶](#schemdraw.elements.transistors.NFet "Link to this definition")

N-type Field Effect Transistor

Parameters:

**bulk** – Draw bulk contact

Anchors:

*   source
    
*   drain
    
*   gate
    
*   center
    

_class_ schemdraw.elements.transistors.NFet2(_\*d_, _bulk: bool \= False_, _\*\*kwargs_)[¶](#schemdraw.elements.transistors.NFet2 "Link to this definition")

N-type Field Effect Transistor which extends source/drain leads to the desired length

Parameters:

**bulk** – Draw bulk contact

Anchors:

*   source
    
*   drain
    
*   gate
    

_class_ schemdraw.elements.transistors.NMos(_\*d_, _diode: bool \= False_, _circle: bool \= False_, _\*\*kwargs_)[¶](#schemdraw.elements.transistors.NMos "Link to this definition")

N-type Metal Oxide Semiconductor Field Effect Transistor

> Args:
> 
> diode: Draw body diode circle: Draw circle around the mosfet
> 
> Anchors:
> 
> *   source
>     
> *   drain
>     
> *   gate
>     

Note: vertical orientation. For horizontal orientation, see NMos2.

_class_ schemdraw.elements.transistors.NMos2(_\*d_, _diode: bool \= False_, _circle: bool \= False_, _\*\*kwargs_)[¶](#schemdraw.elements.transistors.NMos2 "Link to this definition")

N-type Metal Oxide Semiconductor Field Effect Transistor

> Args:
> 
> diode: Draw body diode circle: Draw circle around the mosfet
> 
> Anchors:
> 
> *   source
>     
> *   drain
>     
> *   gate
>     

Note: horizontal orientation. For vertical orientation, see NMos.

_class_ schemdraw.elements.transistors.PFet(_\*d_, _bulk: bool \= False_, _\*\*kwargs_)[¶](#schemdraw.elements.transistors.PFet "Link to this definition")

P-type Field Effect Transistor

Parameters:

**bulk** – Draw bulk contact

Anchors:

source drain gate center

_class_ schemdraw.elements.transistors.PFet2(_\*d_, _bulk: bool \= False_, _\*\*kwargs_)[¶](#schemdraw.elements.transistors.PFet2 "Link to this definition")

P-type Field Effect Transistor which extends source/drain leads to the desired length

Parameters:

**bulk** – Draw bulk contact

Anchors:

*   source
    
*   drain
    
*   gate
    

_class_ schemdraw.elements.transistors.PMos(_\*d_, _diode: bool \= False_, _circle: bool \= False_, _\*\*kwargs_)[¶](#schemdraw.elements.transistors.PMos "Link to this definition")

P-type Metal Oxide Semiconductor Field Effect Transistor

> Args:
> 
> diode: Draw body diode circle: Draw circle around the mosfet
> 
> Anchors:
> 
> *   source
>     
> *   drain
>     
> *   gate
>     

Note: vertical orientation. For horizontal orientation, see PMos2.

_class_ schemdraw.elements.transistors.PMos2(_\*d_, _diode: bool \= False_, _circle: bool \= False_, _\*\*kwargs_)[¶](#schemdraw.elements.transistors.PMos2 "Link to this definition")

P-type Metal Oxide Semiconductor Field Effect Transistor

> Args:
> 
> diode: Draw body diode circle: Draw circle around the mosfet
> 
> Anchors:
> 
> *   source
>     
> *   drain
>     
> *   gate
>     

Note: horizontal orientation. For vertical orientation, see PMos.

#### Transformers[¶](#module-schemdraw.elements.xform "Link to this heading")

Transformer element definitions

_class_ schemdraw.elements.xform.Transformer(_\*d_, _t1: int \= 4_, _t2: int \= 4_, _core: bool \= True_, _loop: bool \= False_, _\*\*kwargs_)[¶](#schemdraw.elements.xform.Transformer "Link to this definition")

Add taps to the windings on either side using the .taps method.

Parameters:

*   **t1** – Turns on primary (left) side
    
*   **t2** – Turns on secondary (right) side
    
*   **core** – Draw the core (parallel lines)
    
*   **loop** – Use spiral/cycloid (loopy) style
    

Anchors:

*   p1: primary side 1
    
*   p2: primary side 2
    
*   s1: secondary side 1
    
*   s2: secondary side 2
    
*   Other anchors defined by taps method
    

tap(_name: str_, _pos: int_, _side: Literal\['primary', 'secondary', 'left', 'right'\] \= 'primary'_)[¶](#schemdraw.elements.xform.Transformer.tap "Link to this definition")

Add a tap

A tap is simply a named anchor definition along one side of the transformer.

Parameters:

*   **name** – Name of the tap/anchor
    
*   **pos** – Turn number from the top of the tap
    
*   **side** – Primary (left) or Secondary (right) side
    

#### Opamp and Integrated Circuits[¶](#module-schemdraw.elements.opamp "Link to this heading")

Operation amplifier

_class_ schemdraw.elements.opamp.Opamp(_\*d_, _sign: bool \= True_, _leads: bool \= False_, _\*\*kwargs_)[¶](#schemdraw.elements.opamp.Opamp "Link to this definition")

Operational Amplifier.

Parameters:

*   **sign** – Draw +/- labels at each input
    
*   **leads** – Draw short leads on input/output
    

Anchors:

*   in1
    
*   in2
    
*   out
    
*   vd
    
*   vs
    
*   n1
    
*   n2
    
*   n1a
    
*   n2a
    

Integrated Circuit Element

_class_ schemdraw.elements.intcircuits.DFlipFlop(_\*d_, _preclr: bool \= False_, _preclrinvert: bool \= True_, _size\=(2, 3)_, _\*\*kwargs_)[¶](#schemdraw.elements.intcircuits.DFlipFlop "Link to this definition")

D-Type Flip Flop

Parameters:

*   **preclr** – Show preset and clear inputs
    
*   **preclrinvert** – Add invert bubble to preset and clear inputs
    
*   **size** – Size of the box
    

Anchors:

*   D
    
*   CLK
    
*   Q
    
*   Qbar
    
*   PRE
    
*   CLR
    

_class_ schemdraw.elements.intcircuits.Ic(_size: Tuple\[float, float\] | Point \= None_, _pins: Sequence\[[IcPin](index.html#schemdraw.elements.intcircuits.IcPin "schemdraw.elements.intcircuits.IcPin")\] \= None_, _pinspacing: float \= 0.6_, _edgepadH: float \= 0.25_, _edgepadW: float \= 0.25_, _leadlen: float \= 0.5_, _lofst: float \= 0.15_, _lsize: float \= 14_, _plblofst: float \= 0.05_, _plblsize: float \= 11_, _slant: float \= 0_, _w: float \= None_, _h: float \= None_, _\*\*kwargs_)[¶](#schemdraw.elements.intcircuits.Ic "Link to this definition")

Integrated Circuit element, or any other black-box element with arbitrary pins on any side.

Parameters:

*   **size** – (Width, Height) of box
    
*   **pins** – List of IcPin instances defining the inputs/outputs
    
*   **pinspacing** – Spacing between pins
    
*   **edgepadH** – Padding between top/bottom and first pin
    
*   **edgepadW** – Padding between left/right and first pin
    
*   **lofst** – Offset between edge and label (inside box)
    
*   **lsize** – Font size of labels (inside box)
    
*   **plblofst** – Offset between edge and pin label (outside box)
    
*   **plblsize** – Font size of pin labels (outside box)
    
*   **slant** – Slant angle of top/bottom edges (e.g. for multiplexers)
    

If a pin is named ‘>’, it will be drawn as a proper clock signal input.

Anchors:

*   inL\[X\] - Each pin on left side
    
*   inR\[X\] - Each pin on right side
    
*   inT\[X\] - Each pin on top side
    
*   inB\[X\] - Each pin on bottom side
    
*   pin\[X\] - Each pin with a number
    
*   CLK (if clock pin is defined with ‘>’ name)
    

Pins with names are also defined as anchors (if the name does not conflict with other attributes).

_class_ schemdraw.elements.intcircuits.Ic555(_\*d_, _\*\*kwargs_)[¶](#schemdraw.elements.intcircuits.Ic555 "Link to this definition")

_class_ schemdraw.elements.intcircuits.IcDIP(_\*d_, _pins: int \= 8_, _names: Sequence\[str\] \= None_, _notch: bool \= True_, _width: float \= 3_, _pinw: float \= 0.6_, _spacing: float \= 0.5_, _number: bool \= True_, _fontsize: float \= 12_, _pfontsize: float \= 10_, _\*\*kwargs_)[¶](#schemdraw.elements.intcircuits.IcDIP "Link to this definition")

Dual-inline Package Integrated Circuit.

Parameters:

*   **pins** – number of pins
    
*   **names** – List of names for each pin to display inside the box
    
*   **notch** – Show the notch at top of box
    
*   **width** – Width of the box
    
*   **pinw** – Width and height of each pin
    
*   **spacing** – Distance between each pin
    
*   **number** – Show pin numbers inside each pin
    
*   **fontsize** – Size for pin name labels
    
*   **pfontsize** – Size for pin number labels
    

Anchors:

*   p\[x\] - Each pin
    
*   p\[x\]\_in - Inside contact for each pin
    

If signal names are provided, they will also be added as anchors along with \_in inside variants.

_class_ schemdraw.elements.intcircuits.IcPin(_name: str | None \= None_, _pin: str | None \= None_, _side: Literal\['top', 'bot', 'lft', 'rgt', 'bottom', 'left', 'right', 'L', 'R', 'T', 'B'\] \= 'L'_, _pos: float | None \= None_, _slot: str | None \= None_, _invert: bool \= False_, _invertradius: float \= 0.15_, _color: str | None \= None_, _rotation: float \= 0_, _anchorname: str | None \= None_, _lblsize: float | None \= None_)[¶](#schemdraw.elements.intcircuits.IcPin "Link to this definition")

Integrated Circuit Pin

Parameters:

*   **name** – Input/output name (inside the box)
    
*   **pin** – Pin name/number (outside the box)
    
*   **side** – Side of box for the pin, ‘left’, ‘right’, ‘top’, ‘bottom’
    
*   **pos** – Pin position along the side, fraction from 0-1
    
*   **slot** – Slot definition of pin location, given in ‘X/Y’ format. ‘2/4’ is the second pin on a side with 4 pins.
    
*   **invert** – Add an invert bubble to the pin
    
*   **invertradius** – Radius of invert bubble
    
*   **color** – Color for the pin and label
    
*   **rotation** – Rotation for label text
    
*   **anchorname** – Named anchor for the pin
    

_class_ schemdraw.elements.intcircuits.JKFlipFlop(_\*d_, _preclr: bool \= False_, _preclrinvert: bool \= True_, _size\=(2, 3)_, _\*\*kwargs_)[¶](#schemdraw.elements.intcircuits.JKFlipFlop "Link to this definition")

J-K Flip Flop

Parameters:

*   **preclr** – Show preset and clear inputs
    
*   **preclrinvert** – Add invert bubble to preset and clear inputs
    
*   **size** – Size of the box
    

Anchors:

*   J
    
*   K
    
*   CLK
    
*   Q
    
*   Qbar
    
*   PRE
    
*   CLR
    

_class_ schemdraw.elements.intcircuits.Multiplexer(_demux: bool \= False_, _size: Tuple\[float, float\] | Point \= None_, _pins: Sequence\[[IcPin](index.html#schemdraw.elements.intcircuits.IcPin "schemdraw.elements.intcircuits.IcPin")\] \= None_, _pinspacing: float \= 0.6_, _edgepadH: float \= 0.25_, _edgepadW: float \= 0.25_, _leadlen: float \= 0.5_, _lofst: float \= 0.15_, _lsize: float \= 14_, _plblofst: float \= 0.05_, _plblsize: float \= 11_, _slant: float \= 25_, _\*\*kwargs_)[¶](#schemdraw.elements.intcircuits.Multiplexer "Link to this definition")

Parameters:

*   **demux** – Draw as demultiplexer
    
*   **size** – (Width, Height) of box
    
*   **pins** – List of IcPin instances defining the inputs/outputs
    
*   **pinspacing** – Spacing between pins
    
*   **edgepadH** – Padding between top/bottom and first pin
    
*   **edgepadW** – Padding between left/right and first pin
    
*   **lofst** – Offset between edge and label (inside box)
    
*   **lsize** – Font size of labels (inside box)
    
*   **plblofst** – Offset between edge and pin label (outside box)
    
*   **plblsize** – Font size of pin labels (outside box)
    
*   **slant** – Slant angle of top/bottom edges
    

If a pin is named ‘>’, it will be drawn as a proper clock signal input.

Anchors:

*   inL\[X\] - Each pin on left side
    
*   inR\[X\] - Each pin on right side
    
*   inT\[X\] - Each pin on top side
    
*   inB\[X\] - Each pin on bottom side
    
*   pin\[X\] - Each pin with a number
    
*   CLK (if clock pin is defined with ‘>’ name)
    

Pins with names are also defined as anchors (if the name does not conflict with other attributes).

_class_ schemdraw.elements.intcircuits.SevenSegment(_\*d_, _decimal: bool \= False_, _digit: int | str \= 8_, _segcolor: str \= 'red'_, _tilt: float \= 10_, _labelsegments: bool \= True_, _anode: bool \= False_, _cathode: bool \= False_, _size\=(2, 1.5)_, _\*\*kwargs_)[¶](#schemdraw.elements.intcircuits.SevenSegment "Link to this definition")

A seven-segment display digit.

Parameters:

*   **decimal** – Show decimal point segment
    
*   **digit** – Number to display
    
*   **segcolor** – Color of segments
    
*   **tilt** – Tilt angle in degrees
    
*   **labelsegments** – Add a-g labels to each segment
    
*   **anode** – Add common anode pin
    
*   **cathode** – Add common cathode pin
    
*   **size** – Total size of the box
    

Anchors:

*   a
    
*   b
    
*   c
    
*   d
    
*   e
    
*   f
    
*   g
    
*   dp
    
*   cathode
    
*   anode
    

_class_ schemdraw.elements.intcircuits.VoltageRegulator(_\*d_, _size\=(2, 1.5)_, _\*\*kwargs_)[¶](#schemdraw.elements.intcircuits.VoltageRegulator "Link to this definition")

Voltage regulator

Parameters:

**size** – Size of the box

Anchors:

*   in
    
*   out
    
*   gnd
    

schemdraw.elements.intcircuits.sevensegdigit(_bottom: float \= 0_, _left: float \= 0_, _seglen: float \= 1.5_, _segw: float \= 0.3_, _spacing: float \= 0.12_, _decimal: bool \= False_, _digit: int | str \= 8_, _segcolor: str \= 'red'_, _tilt: float \= 10_, _labelsegments: bool \= True_) → list\[[Segment](index.html#schemdraw.segments.Segment "schemdraw.segments.Segment") | [SegmentText](index.html#schemdraw.segments.SegmentText "schemdraw.segments.SegmentText") | [SegmentPoly](index.html#schemdraw.segments.SegmentPoly "schemdraw.segments.SegmentPoly") | [SegmentArc](index.html#schemdraw.segments.SegmentArc "schemdraw.segments.SegmentArc") | [SegmentCircle](index.html#schemdraw.segments.SegmentCircle "schemdraw.segments.SegmentCircle") | [SegmentBezier](index.html#schemdraw.segments.SegmentBezier "schemdraw.segments.SegmentBezier")\][¶](#schemdraw.elements.intcircuits.sevensegdigit "Link to this definition")

Generate drawing segments for a 7-segment display digit. Use for building new elements incorporating a 7-segment display.

Parameters:

*   **bottom** – Location of bottom of digit
    
*   **left** – Location of left side of digit
    
*   **seglen** – Length of one segment
    
*   **segw** – Width of one segment
    
*   **spacing** – Distance between segments in corners
    
*   **decimal** – Show decimal point segment
    
*   **digit** – Number to display
    
*   **segcolor** – Color of segments
    
*   **tilt** – Tilt angle in degrees
    
*   **labelsegments** – Add a-g labels to each segment
    
*   **anode** – Add common anode pin
    
*   **cathode** – Add common cathode pin
    
*   **size** – Total size of the box
    

Returns:

List of Segments making the digit

#### Other[¶](#module-schemdraw.elements.misc "Link to this heading")

Other elements

_class_ schemdraw.elements.misc.AudioJack(_\*d_, _radius: float \= 0.075_, _ring: bool \= False_, _ringswitch: bool \= False_, _dots: bool \= True_, _switch: bool \= False_, _open: bool \= True_, _\*\*kwargs_)[¶](#schemdraw.elements.misc.AudioJack "Link to this definition")

Audio Jack with 2 or 3 connectors and optional switches.

Parameters:

*   **ring** – Show ring (third conductor) contact
    
*   **switch** – Show switch on tip contact
    
*   **ringswitch** – Show switch on ring contact
    
*   **dots** – Show connector dots
    
*   **radius** – Radius of connector dots
    

Anchors:

*   tip
    
*   sleeve
    
*   ring
    
*   ringswitch
    
*   tipswitch
    

_class_ schemdraw.elements.misc.Mic(_\*d_, _\*\*kwargs_)[¶](#schemdraw.elements.misc.Mic "Link to this definition")

Microphone element with two inputs.

Anchors:

*   in1
    
*   in2
    

_class_ schemdraw.elements.misc.Motor(_\*d_, _\*\*kwargs_)[¶](#schemdraw.elements.misc.Motor "Link to this definition")

_class_ schemdraw.elements.misc.Speaker(_\*d_, _\*\*kwargs_)[¶](#schemdraw.elements.misc.Speaker "Link to this definition")

Speaker element with two inputs.

Anchors:

*   in1
    
*   in2
    

Compound elements made from groups of other elements

_class_ schemdraw.elements.compound.ElementCompound(_\*d_, _\*\*kwargs_)[¶](#schemdraw.elements.compound.ElementCompound "Link to this definition")

Element onto which other elements can be added like a drawing

add(_element: [Element](index.html#schemdraw.elements.Element "schemdraw.elements.elements.Element")_) → [Element](index.html#schemdraw.elements.Element "schemdraw.elements.elements.Element")[¶](#schemdraw.elements.compound.ElementCompound.add "Link to this definition")

Add an element to the segments list

move(_dx: float \= 0_, _dy: float \= 0_) → None[¶](#schemdraw.elements.compound.ElementCompound.move "Link to this definition")

Move relative to current position

move\_from(_xy: Point_, _dx: float \= 0_, _dy: float \= 0_, _theta: float \= None_) → None[¶](#schemdraw.elements.compound.ElementCompound.move_from "Link to this definition")

Move relative to xy position

_class_ schemdraw.elements.compound.Optocoupler(_\*d_, _box: bool \= True_, _boxfill: str \= 'none'_, _boxpad: float \= 0.2_, _base: bool \= False_, _\*\*kwargs_)[¶](#schemdraw.elements.compound.Optocoupler "Link to this definition")

Optocoupler element

Parameters:

*   **box** – Draw a box around the optocoupler
    
*   **boxfill** – Color to fill the box
    
*   **boxpad** – Padding between phototransistor and box
    
*   **base** – Add a base contact to the phototransistor
    

Anchors:

*   anode
    
*   cathode
    
*   emitter
    
*   collector
    
*   base (if base==True)
    

_class_ schemdraw.elements.compound.Rectifier(_fill\=False_, _labels\=None_, _\*\*kwargs_)[¶](#schemdraw.elements.compound.Rectifier "Link to this definition")

Diode Rectifier Bridge

Parameters:

*   **fill** – Fill the didoes
    
*   **labels** – Labels to draw on each resistor
    

Anchors:

*   N
    
*   S
    
*   E
    
*   W
    

_class_ schemdraw.elements.compound.Relay(_\*d_, _unit: float \= 2_, _cycl: bool \= False_, _switch: str \= 'spst'_, _core: bool \= True_, _box: bool \= True_, _boxfill: str \= 'none'_, _boxpad: float \= 0.25_, _swreverse: bool \= False_, _swflip: bool \= False_, _link: bool \= True_, _\*\*kwargs_)[¶](#schemdraw.elements.compound.Relay "Link to this definition")

Relay element with an inductor and switch

Parameters:

*   **unit** – Unit length of the inductor
    
*   **cycloid** – Use cycloid style inductor
    
*   **switch** – Switch style ‘spst’, ‘spdt’, ‘dpst’, ‘dpdt’
    
*   **swreverse** – Reverse the switch
    
*   **swflip** – Flip the switch up/down
    
*   **core** – Show inductor core bar
    
*   **link** – Show dotted line linking inductor and switch
    
*   **box** – Draw a box around the relay
    
*   **boxfill** – Color to fill the box
    
*   **boxpad** – Spacing between components and box
    

_class_ schemdraw.elements.compound.Wheatstone(_vout: bool \= False_, _labels: Sequence\[str\] \= None_, _\*\*kwargs_)[¶](#schemdraw.elements.compound.Wheatstone "Link to this definition")

Wheatstone Resistor Bridge

Parameters:

*   **vout** – draw output terminals inside the bridge
    
*   **labels** – Labels to draw on each resistor
    

Anchors:

*   N
    
*   S
    
*   E
    
*   W
    
*   vo1 (if vout==True)
    
*   vo2 (if vout==True)
    

Twoport elements made from groups of other elements

_class_ schemdraw.elements.twoports.CurrentTransactor(_\*d_, _reverse\_output: bool \= False_, _\*\*kwargs_)[¶](#schemdraw.elements.twoports.CurrentTransactor "Link to this definition")

Current transactor

Parameters:

*   **bpadx** – Horizontal padding from edge of either component
    
*   **bpady** – Vertical padding from edge of either component
    
*   **minw** – Margin around component if smaller than minw
    
*   **terminals** – Draw with terminals extending past box
    
*   **component\_offset** – Offset between input and output element
    
*   **box** – Draw twoport outline
    
*   **boxfill** – Color to fill the twoport if not None
    
*   **boxlw** – Line width of twoport outline
    
*   **boxls** – Line style of twoport outline ‘-’, ‘–’, ‘:’, etc.
    
*   **reverse\_output** – Switch direction of output source, defaults to False
    

Anchors:

*   in\_p
    
*   in\_n
    
*   out\_p
    
*   out\_n
    
*   center
    

_class_ schemdraw.elements.twoports.ElementTwoport(_\*d_, _input\_element: [Element2Term](index.html#schemdraw.elements.Element2Term "schemdraw.elements.elements.Element2Term")_, _output\_element: [Element2Term](index.html#schemdraw.elements.Element2Term "schemdraw.elements.elements.Element2Term")_, _boxpadx: float \= 0.2_, _boxpady: float \= 0.2_, _minw: float \= 0.5_, _terminals: bool \= True_, _unit: float \= 1.5_, _width: float \= 2.15_, _box: bool \= True_, _boxfill: str \= None_, _boxlw: float \= None_, _boxls: Literal\['-', ':', '--', '-.'\] \= None_, _\*\*kwargs_)[¶](#schemdraw.elements.twoports.ElementTwoport "Link to this definition")

Compound twoport element

Parameters:

*   **input\_element** – The element forming the input branch of the twoport
    
*   **output\_element** – The element forming the output branch of the twoport
    
*   **bpadx** – Horizontal padding from edge of either component
    
*   **bpady** – Vertical padding from edge of either component
    
*   **minw** – Margin around component if smaller than minw
    
*   **terminals** – Draw with terminals extending past box
    
*   **unit** – Length of input and output element
    
*   **width** – Width of the twoport box
    
*   **box** – Draw twoport outline
    
*   **boxfill** – Color to fill the twoport if not None
    
*   **boxlw** – Line width of twoport outline
    
*   **boxls** – Line style of twoport outline ‘-’, ‘–’, ‘:’, etc.
    

Anchors:

*   in\_p
    
*   in\_n
    
*   out\_p
    
*   out\_n
    
*   center
    

_class_ schemdraw.elements.twoports.Nullor(_\*d_, _\*\*kwargs_)[¶](#schemdraw.elements.twoports.Nullor "Link to this definition")

Parameters:

*   **bpadx** – Horizontal padding from edge of either component
    
*   **bpady** – Vertical padding from edge of either component
    
*   **minw** – Margin around component if smaller than minw
    
*   **terminals** – Draw with terminals extending past box
    
*   **component\_offset** – Offset between input and output element
    
*   **box** – Draw twoport outline
    
*   **boxfill** – Color to fill the twoport if not None
    
*   **boxlw** – Line width of twoport outline
    
*   **boxls** – Line style of twoport outline ‘-’, ‘–’, ‘:’, etc.
    

Anchors:

*   in\_p
    
*   in\_n
    
*   out\_p
    
*   out\_n
    
*   center
    

_class_ schemdraw.elements.twoports.TransadmittanceTransactor(_\*d_, _reverse\_output: bool \= False_, _\*\*kwargs_)[¶](#schemdraw.elements.twoports.TransadmittanceTransactor "Link to this definition")

Transadmittance transactor

Parameters:

*   **bpadx** – Horizontal padding from edge of either component
    
*   **bpady** – Vertical padding from edge of either component
    
*   **minw** – Margin around component if smaller than minw
    
*   **terminals** – Draw with terminals extending past box
    
*   **component\_offset** – Offset between input and output element
    
*   **box** – Draw twoport outline
    
*   **boxfill** – Color to fill the twoport if not None
    
*   **boxlw** – Line width of twoport outline
    
*   **boxls** – Line style of twoport outline ‘-’, ‘–’, ‘:’, etc.
    
*   **reverse\_output** – Switch direction of output source, defaults to False
    

Anchors:

*   in\_p
    
*   in\_n
    
*   out\_p
    
*   out\_n
    
*   center
    

_class_ schemdraw.elements.twoports.TransimpedanceTransactor(_\*d_, _reverse\_output: bool \= False_, _\*\*kwargs_)[¶](#schemdraw.elements.twoports.TransimpedanceTransactor "Link to this definition")

Transimpedance transactor

Parameters:

*   **bpadx** – Horizontal padding from edge of either component
    
*   **bpady** – Vertical padding from edge of either component
    
*   **minw** – Margin around component if smaller than minw
    
*   **terminals** – Draw with terminals extending past box
    
*   **component\_offset** – Offset between input and output element
    
*   **box** – Draw twoport outline
    
*   **boxfill** – Color to fill the twoport if not None
    
*   **boxlw** – Line width of twoport outline
    
*   **boxls** – Line style of twoport outline ‘-’, ‘–’, ‘:’, etc.
    
*   **reverse\_output** – Switch direction of output source, defaults to False
    

Anchors:

*   in\_p
    
*   in\_n
    
*   out\_p
    
*   out\_n
    
*   center
    

_class_ schemdraw.elements.twoports.TwoPort(_\*d_, _sign: bool \= True_, _arrow: bool \= True_, _reverse\_output: bool \= False_, _\*\*kwargs_)[¶](#schemdraw.elements.twoports.TwoPort "Link to this definition")

Generic Twoport

Parameters:

*   **bpadx** – Horizontal padding from edge of either component
    
*   **bpady** – Vertical padding from edge of either component
    
*   **minw** – Margin around component if smaller than minw
    
*   **terminals** – Draw with terminals extending past box
    
*   **component\_offset** – Offset between input and output element
    
*   **box** – Draw twoport outline
    
*   **boxfill** – Color to fill the twoport if not None
    
*   **boxlw** – Line width of twoport outline
    
*   **boxls** – Line style of twoport outline ‘-’, ‘–’, ‘:’, etc.
    
*   **sign** – Draw input and output terminal labels
    
*   **arrow** – Draw arrow from input to output
    

Anchors:

*   in\_p
    
*   in\_n
    
*   out\_p
    
*   out\_n
    
*   center
    

_class_ schemdraw.elements.twoports.VMCMPair(_\*d_, _\*\*kwargs_)[¶](#schemdraw.elements.twoports.VMCMPair "Link to this definition")

Nullor

Parameters:

*   **bpadx** – Horizontal padding from edge of either component
    
*   **bpady** – Vertical padding from edge of either component
    
*   **minw** – Margin around component if smaller than minw
    
*   **terminals** – Draw with terminals extending past box
    
*   **component\_offset** – Offset between input and output element
    
*   **box** – Draw twoport outline
    
*   **boxfill** – Color to fill the twoport if not None
    
*   **boxlw** – Line width of twoport outline
    
*   **boxls** – Line style of twoport outline ‘-’, ‘–’, ‘:’, etc.
    

Anchors:

*   in\_p
    
*   in\_n
    
*   out\_p
    
*   out\_n
    
*   center
    

_class_ schemdraw.elements.twoports.VoltageTransactor(_\*d_, _reverse\_output: bool \= False_, _\*\*kwargs_)[¶](#schemdraw.elements.twoports.VoltageTransactor "Link to this definition")

Voltage transactor

Parameters:

*   **bpadx** – Horizontal padding from edge of either component
    
*   **bpady** – Vertical padding from edge of either component
    
*   **minw** – Margin around component if smaller than minw
    
*   **terminals** – Draw with terminals extending past box
    
*   **component\_offset** – Offset between input and output element
    
*   **box** – Draw twoport outline
    
*   **boxfill** – Color to fill the twoport if not None
    
*   **boxlw** – Line width of twoport outline
    
*   **boxls** – Line style of twoport outline ‘-’, ‘–’, ‘:’, etc.
    
*   **reverse\_output** – Switch direction of output source, defaults to False
    

Anchors:

*   in\_p
    
*   in\_n
    
*   out\_p
    
*   out\_n
    
*   center
    

### Logic Gates[¶](#module-schemdraw.logic.logic "Link to this heading")

Logic gate definitions

_class_ schemdraw.logic.logic.And(_\*d_, _inputs: int \= 2_, _nand: bool \= False_, _inputnots: Sequence\[int\] \= None_, _leadin: float \= 0.35_, _leadout: float \= 0.35_, _\*\*kwargs_)[¶](#schemdraw.logic.logic.And "Link to this definition")

AND gate

Parameters:

*   **inputs** – Number of inputs to gate.
    
*   **nand** – Draw invert bubble on output
    
*   **inputnots** – Input numbers (starting at 1) of inputs that have invert bubble
    
*   **leadin** – Length of input leads
    
*   **leadout** – Length of output lead
    

Anchors:

out in\[X\] - for each input

_class_ schemdraw.logic.logic.Buf(_\*d_, _\*\*kwargs_)[¶](#schemdraw.logic.logic.Buf "Link to this definition")

Buffer

Anchors:

in out

_class_ schemdraw.logic.logic.Not(_\*d_, _\*\*kwargs_)[¶](#schemdraw.logic.logic.Not "Link to this definition")

Not gate/inverter

Anchors:

in out

_class_ schemdraw.logic.logic.NotNot(_\*d_, _\*\*kwargs_)[¶](#schemdraw.logic.logic.NotNot "Link to this definition")

Double inverter

Anchors:

in out

_class_ schemdraw.logic.logic.Or(_\*d_, _inputs: int \= 2_, _nor: bool \= False_, _xor: bool \= False_, _inputnots: Sequence\[int\] \= None_, _leadin: float \= 0.35_, _leadout: float \= 0.35_, _\*\*kwargs_)[¶](#schemdraw.logic.logic.Or "Link to this definition")

OR or XOR gate element.

Parameters:

*   **inputs** – Number of inputs to gate.
    
*   **nor** – Draw invert bubble on output
    
*   **xor** – Draw as exclusive-or gate
    
*   **inputnots** – Input numbers (starting at 1) of inputs that have invert bubble
    
*   **leadin** – Length of input leads
    
*   **leadout** – Length of output lead
    

Anchors:

out in\[X\] - for each input

_class_ schemdraw.logic.logic.Schmitt(_\*d_, _\*\*kwargs_)[¶](#schemdraw.logic.logic.Schmitt "Link to this definition")

Schmitt Trigger

Anchors:

in out

_class_ schemdraw.logic.logic.SchmittAnd(_\*d_, _leadin: float \= 0.35_, _leadout: float \= 0.35_, _\*\*kwargs_)[¶](#schemdraw.logic.logic.SchmittAnd "Link to this definition")

Schmitt Trigger AND

Anchors:

in1 in2 out

_class_ schemdraw.logic.logic.SchmittNot(_\*d_, _\*\*kwargs_)[¶](#schemdraw.logic.logic.SchmittNot "Link to this definition")

Inverted Schmitt Trigger

Anchors:

in out

_class_ schemdraw.logic.logic.Tgate(_\*d_, _\*\*kwargs_)[¶](#schemdraw.logic.logic.Tgate "Link to this definition")

Transmission gate.

Anchors:

in out c cbar

_class_ schemdraw.logic.logic.Tristate(_\*d_, _\*\*kwargs_)[¶](#schemdraw.logic.logic.Tristate "Link to this definition")

Tristate inverter

Anchors:

in out c

logic\_parser.logicparse(_gateW: float \= 2_, _gateH: float \= 0.75_, _outlabel: str \= None_) → [Drawing](index.html#schemdraw.Drawing "schemdraw.schemdraw.Drawing")[¶](#schemdraw.parsing.logic_parser.logicparse "Link to this definition")

Parse a logic string expression and draw the gates in a schemdraw Drawing

Logic expression is defined by string using ‘and’, ‘or’, ‘not’, etc. for example, “a or (b and c)”. Parser recognizes several symbols and names for logic functions: \[and, ‘&’, ‘∧’\] \[or, ‘|’, ‘∨’, ‘+’\] \[xor, ‘⊕’, ‘⊻’\] \[not, ‘~’, ‘¬’\]

Parameters:

*   **expr** – Logic expression
    
*   **gateH** – Height of one gate
    
*   **gateW** – Width of one gate
    
*   **outlabel** – Label for logic output
    

Returns:

schemdraw.Drawing with logic tree

_class_ schemdraw.logic.table.Table(_table: str_, _colfmt: str \= None_, _fontsize: float \= 12_, _font: str \= 'sans'_, _\*\*kwargs_)[¶](#schemdraw.logic.table.Table "Link to this definition")

Table Element for drawing rudimentary Markdown formatted tables, such as logic truth tables.

Parameters:

*   **table** – Table definition, as markdown string. Columns separated by |. Separator rows contain — or === between column separators.
    
*   **colfmt** – Justification and vertical separators to draw for each column, similar to LaTeX tabular environment parameter. Justification characters include ‘c’, ‘r’, and ‘l’ for center, left, and right justification. Separator characters may be ‘|’ for a single vertical bar, or ‘||’ or ‘ǁ’ for a double vertical bar, or omitted for no bar. Example: ‘cc|c’.
    
*   **fontsize** – Point size of table font
    
*   **font** – Name of table font
    

Example Table:

| A | B | Y | |—|—|—| | 0 | 0 | 1 | | 0 | 1 | 0 | | 1 | 0 | 0 | | 1 | 1 | 0 |

_class_ schemdraw.logic.kmap.Kmap(_names: str \= 'ABCD'_, _truthtable: Sequence\[Sequence\[int | str\]\] \= None_, _groups: dict \= None_, _default: str \= '0'_, _\*\*kwargs_)[¶](#schemdraw.logic.kmap.Kmap "Link to this definition")

Karnaugh Map

Draws a K-Map with 2, 3, or 4 variables.

Parameters:

*   **names** – 2, 3, or 4-character string defining names of the inputs
    
*   **truthtable** – list defining values to display in each box of the K-Map. First element is string of 2, 3, or 4 logic 0’s and 1’s, and last element is the string to display for that input. Example: (‘0000’, ‘1’) displays a ‘1’ when all inputs are 0.
    
*   **groups** – dictionary of style parameters for circling groups of inputs. Dictionary key must be same length as names, and defines which elements are circled using ‘0’, ‘1’, or ‘.’ in each position. For example, ‘1…’ circles every box where A=1, and ‘.11.’ circles every box where both B and C are 1. Value of dictionary pair is another dictionary containing style of box (e.g. color, fill, lw, and ls).
    
*   **default** – string to display in boxes that don’t have a truthtable entry defined
    

Anchors:

*   cellXXXX - Center of each cell in the grid, where X is 0 or 1
    

_class_ schemdraw.logic.timing.TimingDiagram(_waved: dict\[str, str\]_, _\*\*kwargs_)[¶](#schemdraw.logic.timing.TimingDiagram "Link to this definition")

Logic Timing Diagram

Draw timing diagrams compatible with WaveJSON format See [https://wavedrom.com/](https://wavedrom.com/) for details. Use from\_json to use WaveJSON strings copied from the site (since they can’t be copied as proper Python dicts due to lack of quoting).

Schemdraw provides a few additional extensions to the WaveJSON dictionary, including asynchronous waveforms and configuration options (color, lw) on each wave. See documentation for full specification.

Parameters:

**wave** – WaveJSON as a Python dict

Keyword Arguments:

*   **yheight** – Height of one waveform
    
*   **ygap** – Separation between two waveforms
    
*   **risetime** – Rise/fall time for wave transitions
    
*   **fontsize** – Size of label fonts
    
*   **nodesize** – Size of node labels
    
*   **namecolor** – Color for wave names
    
*   **datacolor** – Color for wave data text
    
*   **nodecolor** – Color for node text
    
*   **gridcolor** – Color of background grid
    

### Digital Signal Processing[¶](#module-schemdraw.dsp.dsp "Link to this heading")

Signal processing elements

_class_ schemdraw.dsp.dsp.Adc(_\*d_, _\*\*kwargs_)[¶](#schemdraw.dsp.dsp.Adc "Link to this definition")

Analog to digital converter

Anchors:

*   in
    
*   out
    
*   E (same as in)
    
*   W (same as out)
    

_class_ schemdraw.dsp.dsp.Amp(_\*d_, _\*\*kwargs_)[¶](#schemdraw.dsp.dsp.Amp "Link to this definition")

Amplifier

Anchors:

*   in
    
*   out
    

_class_ schemdraw.dsp.dsp.Circle(_\*d_, _\*\*kwargs_)[¶](#schemdraw.dsp.dsp.Circle "Link to this definition")

Empty circle element

Anchors:

*   N
    
*   S
    
*   E
    
*   W
    
*   NW
    
*   NE
    
*   SW
    
*   SE
    

_class_ schemdraw.dsp.dsp.Circulator(_circle with an arrow in it_)[¶](#schemdraw.dsp.dsp.Circulator "Link to this definition")

Anchors:

*   N
    
*   S
    
*   E
    
*   W
    

_class_ schemdraw.dsp.dsp.Dac(_\*d_, _\*\*kwargs_)[¶](#schemdraw.dsp.dsp.Dac "Link to this definition")

Digital to analog converter

Anchors:

*   in
    
*   out
    
*   E (same as in)
    
*   W (same as out)
    

_class_ schemdraw.dsp.dsp.Demod(_\*d_, _\*\*kwargs_)[¶](#schemdraw.dsp.dsp.Demod "Link to this definition")

Demodulator (box with a diode in it)

Anchors:

*   N
    
*   S
    
*   E
    
*   W
    

_class_ schemdraw.dsp.dsp.Filter(_\*d_, _response: Literal\['lp', 'bp', 'hp', 'notch'\] \= None_, _\*\*kwargs_)[¶](#schemdraw.dsp.dsp.Filter "Link to this definition")

Parameters:

**response** – Filter response (‘lp’, ‘bp’, ‘hp’, or ‘notch’) for low-pass, band-pass, high-pass, and notch/band-stop filters

Anchors:

*   N
    
*   S
    
*   E
    
*   W
    

_class_ schemdraw.dsp.dsp.Isolator(_box with an arrow in it_)[¶](#schemdraw.dsp.dsp.Isolator "Link to this definition")

Anchors:

*   N
    
*   S
    
*   E
    
*   W
    

_class_ schemdraw.dsp.dsp.Mixer(_\*d_, _N: str \= None_, _E: str \= None_, _S: str \= None_, _W: str \= None_, _font: str \= None_, _fontsize: float \= 10_, _\*\*kwargs_)[¶](#schemdraw.dsp.dsp.Mixer "Link to this definition")

Parameters:

*   **N** – text in North sector
    
*   **S** – text in South sector
    
*   **E** – text in East sector
    
*   **W** – text in West sector
    
*   **font** – Font family/name
    
*   **fontsize** – Point size of label font
    

Anchors:

*   N
    
*   S
    
*   E
    
*   W
    
*   NW
    
*   NE
    
*   SW
    
*   SE
    

_class_ schemdraw.dsp.dsp.Oscillator(_\*d_, _\*\*kwargs_)[¶](#schemdraw.dsp.dsp.Oscillator "Link to this definition")

Oscillator in a circle

Anchors:

*   N
    
*   S
    
*   E
    
*   W
    
*   NW
    
*   NE
    
*   SW
    
*   SE
    

_class_ schemdraw.dsp.dsp.OscillatorBox(_\*d_, _\*\*kwargs_)[¶](#schemdraw.dsp.dsp.OscillatorBox "Link to this definition")

Oscillator in a square

Anchors:

*   N
    
*   S
    
*   E
    
*   W
    

_class_ schemdraw.dsp.dsp.Speaker(_\*d_, _\*\*kwargs_)[¶](#schemdraw.dsp.dsp.Speaker "Link to this definition")

Speaker with only one terminal

_class_ schemdraw.dsp.dsp.Square(_\*d_, _\*\*kwargs_)[¶](#schemdraw.dsp.dsp.Square "Link to this definition")

Empty square element

Anchors:

*   N
    
*   S
    
*   E
    
*   W
    

_class_ schemdraw.dsp.dsp.Sum(_\*d_, _\*\*kwargs_)[¶](#schemdraw.dsp.dsp.Sum "Link to this definition")

Summation element (+ symbol)

Anchors:

*   N
    
*   S
    
*   E
    
*   W
    
*   NW
    
*   NE
    
*   SW
    
*   SE
    

_class_ schemdraw.dsp.dsp.SumSigma(_\*d_, _\*\*kwargs_)[¶](#schemdraw.dsp.dsp.SumSigma "Link to this definition")

Summation element (Greek Sigma symbol)

Anchors:

*   N
    
*   S
    
*   E
    
*   W
    
*   NW
    
*   NE
    
*   SW
    
*   SE
    

_class_ schemdraw.dsp.dsp.VGA(_tuneup: bool \= True_, _\*d_, _\*\*kwargs_)[¶](#schemdraw.dsp.dsp.VGA "Link to this definition")

Variable Gain Amplifier (amplifier symbol with an arrow over it)

Parameters:

**tuneup** – Set tune above or below the symbol

Anchors:

*   input
    
*   out
    
*   tune
    

### Flowcharting[¶](#module-schemdraw.flow.flow "Link to this heading")

Flowcharting element definitions

_class_ schemdraw.flow.flow.Box(_w: float \= 3_, _h: float \= 2_, _\*\*kwargs_)[¶](#schemdraw.flow.flow.Box "Link to this definition")

Flowchart Process Box

Parameters:

*   **w** – Width of box
    
*   **h** – Height of box
    

Anchors:

*   16 compass points (N, S, E, W, NE, NNE, etc.)
    

schemdraw.flow.flow.Circle[¶](#schemdraw.flow.flow.Circle "Link to this definition")

alias of [`Connect`](#schemdraw.flow.flow.Connect "schemdraw.flow.flow.Connect")

_class_ schemdraw.flow.flow.Connect(_r: float \= 0.75_, _\*\*kwargs_)[¶](#schemdraw.flow.flow.Connect "Link to this definition")

Flowchart connector/circle

Parameters:

**r** – Radius of circle

Anchors:

*   16 compass points (N, S, E, W, NE, NNE, etc.)
    

_class_ schemdraw.flow.flow.Data(_w: float \= 3_, _h: float \= 2_, _s: float \= 0.5_, _\*\*kwargs_)[¶](#schemdraw.flow.flow.Data "Link to this definition")

Flowchart data or input/output box (parallelogram)

Parameters:

*   **w** – Width of box
    
*   **h** – Height of box
    
*   **s** – slant of sides
    

Anchors:

*   16 compass points (N, S, E, W, NE, NNE, etc.)
    

_class_ schemdraw.flow.flow.Decision(_w: float \= 4_, _h: float \= 2_, _N: str \= None_, _E: str \= None_, _S: str \= None_, _W: str \= None_, _font: str \= None_, _fontsize: float \= 14_, _\*\*kwargs_)[¶](#schemdraw.flow.flow.Decision "Link to this definition")

Flowchart decision (diamond)

Parameters:

*   **w** – Width of box
    
*   **h** – Height of box
    
*   **N** – text for North decision branch
    
*   **S** – text for South decision branch
    
*   **E** – text for East decision branch
    
*   **W** – text for West decision branch
    
*   **font** – Font family/name
    
*   **fontsize** – Point size of label font
    

Anchors:

*   16 compass points (N, S, E, W, NE, NNE, etc.)
    

_class_ schemdraw.flow.flow.Ellipse(_w: float \= 3_, _h: float \= 2_, _\*\*kwargs_)[¶](#schemdraw.flow.flow.Ellipse "Link to this definition")

Flowchart ellipse

Parameters:

*   **w** – Width of ellipse
    
*   **h** – Height of ellipse
    

Anchors:

*   16 compass points (N, S, E, W, NE, NNE, etc.)
    

schemdraw.flow.flow.Process[¶](#schemdraw.flow.flow.Process "Link to this definition")

alias of [`Box`](#schemdraw.flow.flow.Box "schemdraw.flow.flow.Box")

_class_ schemdraw.flow.flow.RoundBox(_w: float \= 3_, _h: float \= 2_, _cornerradius: float \= 0.3_, _\*\*kwargs_)[¶](#schemdraw.flow.flow.RoundBox "Link to this definition")

Alternate Process box with rounded corners

Parameters:

*   **w** – Width of box
    
*   **h** – Height of box
    

Anchors:

*   16 compass points (N, S, E, W, NE, NNE, etc.)
    

schemdraw.flow.flow.RoundProcess[¶](#schemdraw.flow.flow.RoundProcess "Link to this definition")

alias of [`RoundBox`](#schemdraw.flow.flow.RoundBox "schemdraw.flow.flow.RoundBox")

schemdraw.flow.flow.Start[¶](#schemdraw.flow.flow.Start "Link to this definition")

alias of [`Terminal`](#schemdraw.flow.flow.Terminal "schemdraw.flow.flow.Terminal")

schemdraw.flow.flow.State[¶](#schemdraw.flow.flow.State "Link to this definition")

alias of [`Connect`](#schemdraw.flow.flow.Connect "schemdraw.flow.flow.Connect")

_class_ schemdraw.flow.flow.StateEnd(_r: float \= 0.75_, _dr\=0.15_, _\*\*kwargs_)[¶](#schemdraw.flow.flow.StateEnd "Link to this definition")

End/Accept State (double circle)

Parameters:

*   **r** – radius
    
*   **dr** – distance between circles
    

Anchors:

*   16 compass points (N, S, E, W, NE, NNE, etc.)
    

_class_ schemdraw.flow.flow.Subroutine(_w: float \= 3.5_, _h: float \= 2_, _s: float \= 0.3_, _\*\*kwargs_)[¶](#schemdraw.flow.flow.Subroutine "Link to this definition")

Flowchart subroutine/predefined process. Box with extra vertical lines near sides.

Parameters:

*   **w** – Width of box
    
*   **h** – Height of box
    
*   **s** – spacing of side lines
    

Anchors:

*   16 compass points (N, S, E, W, NE, NNE, etc.)
    

_class_ schemdraw.flow.flow.Terminal(_w: float \= 3_, _h: float \= 1.25_, _\*\*kwargs_)[¶](#schemdraw.flow.flow.Terminal "Link to this definition")

Flowchart start/end terminal

Parameters:

*   **w** – Width of box
    
*   **h** – Height of box
    

Anchors:

*   16 compass points (N, S, E, W, NE, NNE, etc.)
    

Change Log[¶](#change-log "Link to this heading")
-------------------------------------------------

v0.17 - 2023-06-03

> New Elements:
> 
> *   Tristate inverter (credit: Jan Genoe)
>     
> *   NMos and PMos elements (credit: dtmaidenmueller)
>     
> *   AnalogNFet, AnalogPFet, AnalogBiasedFet
>     
> *   DataBusLine
>     
> *   CurrentMirror, VoltageMirror
>     
> *   Nullator, Norator, VMCMPair
>     
> *   Compound twoport elements (ElementTwoport base class):
>     
>     *   TwoPort
>         
>     *   VoltageTransactor
>         
>     *   TransimpedanceTransactor
>         
>     *   CurrentTransactor
>         
>     *   TransadmittanceTransactor
>         
>     *   Nullor
>         
>     
> 
> Enhancements:
> 
> *   Added arguments for length/width of CurrentLabel arrows (credit: Christian Seigel)
>     
> *   Added config option for setting whitespace margins
>     
> 
> Bug fixes:
> 
> *   Fixed regression bug in logicparse where labels were not drawn on inputs/outputs
>     
> *   Fix timing diagrams when async times are longer than the wave
>     
> *   Fixed default style hierarchy on segments
>     
> *   Fixed CurrentLabel placement with transistor elements, now follows biasing current
>     
> *   Fixed CurrentLabel positioning for elements with no center anchor
>     
> 
> Other changes:
> 
> *   Deprecated positional direction parameter to Element class.
>     
> *   Add nonglobal rotation mode attribute to SegmentText
>     

v0.16 - 25-Mar-2023

> *   Added canvas parameter to Drawing and draw method, and deprecated backend parameter.
>     
> *   Removed elements argument from Drawing. Use Drawing.add\_elements.
>     
> *   Added Drawing.set\_anchor to define anchor points, useful for ElementDrawing instances.
>     
> *   Added shunt resistor symbol Rshunt
>     
> *   Fixed lead length of XOR gates to align with OR gates
>     
> *   Fixed greater and less than symbols in SVG backend
>     
> *   Fixed some anchor positions on flowchart symbols
>     
> *   Allow font parameter to be the path of a TTF file
>     
> *   Removed old deprecations
>     
> *   Replaced setup.py with setup.cfg
>     

v0.15 - 20-Jun-2022

> *   Added DSP elements Circulator, Isolator, VGA
>     
> *   Added ZLabel element for right-angle impedance arrow labels
>     
> *   Changed DSP anchor names from ‘in’ to ‘input’ to avoid conflict with ‘in’ keyword
>     
> *   Fixed styles with nested ElementDrawing elements
>     
> *   Fixed zorder of filled elements in Matplotlib backend
>     
> *   Added mathfont parameter to labels for specifying different font on math labels
>     
> *   Added padx and pady parameters to Encircle elements
>     
> *   Moved SVG backend configuration to svgconfig object and deprecated ‘settextmode’.
>     
> *   Added ‘visible’ parameter to Segment objects
>     

v0.14 - 09-Jan-2022

> *   Added context manager to Drawing class.
>     
> *   Added Wire element for quick 90-degree connections
>     
> *   Added Encircle, EncircleBox, and Annotate elements
>     
> *   Added Wheatstone, Rectifier, SparkGap elements
>     
> *   Added “2T” version of transistor elements for placement as as two-terminal elements
>     
> *   tox and toy methods automatically change drawing direction, removing need to specify right() and tox(), for example.
>     
> *   Added istart and iend anchors to 2-Terminal elements for defining inner start and end points before lead extensions
>     
> *   Added dot and idot methods to two-terminal elements
>     
> *   Added ‘-o’ and ‘-|’ arrow types to draw dot or endcap instead of arrow at the end of lines
>     
> *   Added leads parameter to OpAmp for adding lead extensions
>     
> *   Added lead parameter to Grounds, Vss, and Vdd
>     
> *   Added optional dx and dy parameters to to and at methods for quick fine-tuning of placement
>     
> *   Added optional length parameter to up, down, left, and right on two-terminal elements
>     
> *   Improved placement of CurrentLabel arrows
>     
> *   Fix default label position on Vss element
>     
> *   Fix positioning of switch contact bubbles
>     
> *   Fix text rotation in svg backend and path mode
>     
> *   The scale method now maintains the length of two-terminal elements
>     

v0.13 - 19-Dec-2021

> *   Added Digital Timing Diagram elements
>     
> *   Added Table and Kmap elements
>     
> *   Added Arc2, Arc3, ArcN, ArcZ, ArcLoop elements, useful for state machine diagrams
>     
> *   Added drop method to Element class to specify where to leave the drawing position
>     
> *   Added move\_from method to Drawing class to move relative to another element anchor
>     
> *   Added more anchors to all flowchart elements
>     
> *   Improved layout of flowchart elements. **May affect layout of some existing flowchart diagrams.**
>     
> *   Added SegmentBezier for creating elements with curves
>     
> *   Deprecated SegmentArrow in favor of Segment with arrow parameter
>     

v0.12 - 05-Nov-2021

> *   Fixed Arrow and LineDot element placement when placed with anchor
>     
> *   Fixed copy/pickle of Element class
>     
> *   Fixed importing \* from schemdraw.elements
>     

v0.11 - 10-Jul-2021

> *   Fixed placing elements by anchor when anchors were defined using a tuple rather than Point
>     
> *   SVG backend adds option for SVG1.x format for better compatibility with SVG renderers
>     
> *   Restore compabitliiby with Python 3.7 via conditional import of typing\_extensions.
>     

v0.10 - 30-Apr-2021

> *   Added options to place labels inside Mixer elements
>     
> *   Fixed arrowhead overshoot
>     
> *   Fixed get\_imagedata function
>     
> *   Update pip install to include optional dependencies
>     
> *   Added ziamath optional dependency for rendering math in SVG backend
>     
> *   Added LoopArrow as superclass of LoopCurrent, for placing a loop anywhere
>     

v0.9.1 - 30-Jan-2021

> *   Fixed missing module in setup.py.
>     

v0.9 - 30-Jan-2021

> *   Added optional SVG backend for drawing directly to an SVG image
>     
> *   Implemented method-chaining “fluent” interface for building elements
>     
> *   Added elements.style method for setting U.S. or European/IEC resistor style
>     
> *   Added parameter for drawing schematic on existing matplotlib axis
>     
> *   Added string parser for creating logic diagrams from expressions like “A or B”
>     
> *   Fixed zooming of arc segments
>     
> *   Added type annotations
>     
> *   Added Drawing.move method for moving cursor by dx and dy.
>     
> *   Drawing class implements += operator, so elements can be added by Drawing += Element()
>     
> *   Removed dependency on Numpy
>     
> *   Added Drawing.interactive\` to allow element-by-element drawing with Matplotlib’s plt.ion().
>     
> *   Now requires Python 3.8+
>     
> *   New Elements:
>     
>     *   CPE (Constant Phase Element)
>         
>     *   Varactor
>         
>     *   FuseIEEE
>         
>     *   FuseIEC
>         
>     *   SwitchRotary
>         
>     *   SwitchReed
>         
>     *   Jack
>         
>     *   Plug
>         
>     *   Ic555
>         
>     *   IcDIP
>         
>     *   SevenSegment
>         
>     *   Outlet Elements
>         
>     
> *   Deprecations:
>     
>     *   Element.add\_label is deprecated (use Element.label)
>         
>     *   Drawing.loopI is deprecated (add a LoopCurrent element)
>         
>     *   Drawing.labelI is deprecated (add a CurrentLabel element)
>         
>     *   Drawing.labelI\_inline is deprecated (add a CurrentLabelInline element)
>         
>     

v0.8 - 15-Aug-2020

> *   Changed Header anchors to pinN for consistency with Ic.
>     
> *   Improved label placement with respect to anchor positions.
>     
> *   Prevent duplicate figures from showing in Jupyter Element representation
>     
> *   Improvements for headless server operation to prevent popup window
>     
> *   Added some undocumented features to documentation
>     
> *   Added Drawing.get\_imagedata function for returning raw image bytes
>     
> *   Fixed pip installation issue with module capitalization. Must import lowercase schemdraw.
>     

v0.7.1 - 26-Jun-2020

> *   Bug fix: restore usage outside of Jupyter, so that Matplotlib window is shown when calling Drawing.draw().
>     

v0.7 - 21-Jun-2020

> *   Dropped support for Python 2. Now requires 3.7+.
>     
> *   Elements are now subclasses of Element. Previous (dict) element names are translated into new class names. Any user-defined elements will need to be converted to classes. The group\_elements function is replaced with ElementDrawing class.
>     
> *   Allow fontsize or size keyword arguments interchangeably in Drawing and add\_label
>     
> *   Updated flow.Decision to use keyword arguments for labeling decision branches
>     
> *   The Ic element label offset parameter changed from lblofst to lofst to avoid conflict with the main element label.
>     
> *   Direct access to Drawing.fig and Drawing.ax are no longer available. Instead, Drawing.draw() returns a schemdraw.Figure instance with fig and ax attributes.
>     
> *   Implemented Jupyter representation functions for both Drawing and Element classes.
>     
> *   New Elements:
>     
>     *   Coax
>         
>     *   Triax
>         
>     *   SwitchDpst
>         
>     *   SwitchDpdt
>         
>     *   Relay
>         
>     *   Optocoupler
>         
>     *   Arrow
>         
>     *   LineDot
>         
>     *   Breaker
>         
>     *   OrthoLines
>         
>     *   RightLines
>         
>     *   BusConnect
>         
>     *   BusLine
>         
>     *   Tag
>         
>     *   Photoresistor
>         
>     *   PhotoresistorBox
>         
>     *   Thermistor
>         
>     *   DiodeShockley
>         
>     *   PotBox
>         
>     *   RBoxVar
>         
>     *   Solar
>         
>     *   Neon
>         
>     *   SourceSquare
>         
>     *   AntennaLoop
>         
>     *   AntennaLoop2
>         
>     *   AudioJack
>         
>     *   Tgate
>         
>     *   Schmitt
>         
>     *   SchmittNot
>         
>     *   SchmittAnd
>         
>     *   SchmittNand
>         
>     

v0.6.0, 11-Feb-2020

> *   Refactored internals to allow more control over individual components of drawing. Should have no effect unless the user is accessing internal attributes of the Element object. This also adds the segments list to the Element object, which allows finer control over individual bits of the drawing.
>     
> *   Updated add\_label so that “top” labels should always appear on top, regardless of flip/reverse
>     
> *   Swapped the direction of current sources, so that a current source with direction “up” has the arrow pointing up.
>     
> *   Added “zorder” parameter in the element definition dictionary and add method
>     
> *   Added elements.ic and elements.multiplexer functions as replacements to blackbox and mux. These include more functionality such as adjusting indiviudal pin rotation, color, and inverter bubbles.
>     
> *   Labels can be placed relative to an anchor position using the add\_label method. This could be useful, for example, in labeling pin numbers on a logic gate or opamp.
>     
> *   Added new anchors to OPAMPs for power supply and offset nulls.
>     
> *   New Elements:
>     
>     *   MIC
>         
>     *   MOTOR
>         
>     
> *   Documentation:
>     
>     *   Upgraded documentation to Sphinx and moved to readthedocs.org at [https://schemdraw.readthedocs.io/en/latest/](https://schemdraw.readthedocs.io/en/latest/).
>         
>     *   Changed preferred import to import SchemDraw.elements as elm. Apparently some people still use import \* with pylab; this suggestion will help avoid conflicts.
>         
>     

v0.5.0, 21-Jul-2019

*   Added flowcharting symbol methods to SchemDraw.flow module
    
*   Added signal processing symbols to SchemDraw.dsp module
    
*   Implemented fill parameter on Drawing.add to fill shapes and closed paths with a solid color
    
*   New elements:
    
    *   Fuse
        
    *   CapacitorVar,
        
    *   DiodeTunnel
        
    *   Jfet
        
    *   Diac
        
    *   Triac
        
    *   SCR
        
    

v0.4.0, 03-Nov-2018

*   Fixed drawing of NOT and related gates to property extend the path
    
*   Fixed arrow translation when grouping elements
    
*   Fixed sidelabels and plabels of blackbox when empty
    
*   Fixed arc drawing due to change in Matplotlib 2.2 on asymmetric partial arcs
    

v0.3.0, 03-Jul-2017

*   Added function for drawing multiplexers/demultiplexers
    
*   Updates to labelI() method to allow reversing arrow and changing length
    
*   Add CSS to documentation
    
*   New elements:
    
    *   PHOTODIODE
        
    *   NFET4
        
    *   PFET4
        
    *   VSS
        
    *   VDD
        
    

v0.2.2, 06-Mar-2016

*   Documentation updates
    
*   New elements:
    
    *   Transformer
        
    *   Josephson Junction (JJ)
        
    

v0.2.1, 03-May-2015

*   Fixed anchor names when element overwrites base anchor, such as BJT\_PNP.
    
*   Added showplot keyword to draw() for non-interactive mode.
    
*   Added 2-collector BJT.
    
*   Documentation: added gallery of schematics.
    

v0.2.0, 29-Apr-2015

*   Added default line width argument to drawing() class. Default width is now 1.5.
    
*   Converted documentation to use all vector-based images
    
*   Added XKCD-mode example
    
*   New elements:
    
    *   BATTERY
        
    *   BAT\_CELL
        
    *   SPEAKER
        
    *   BUTTON
        
    *   BUTTON\_NC
        
    *   XTAL
        
    *   MEMRISTOR,
        
    *   SCHOTTKY
        
    *   ZENER
        
    *   LED2
        
    

v0.1.4, 30-Sep-2014

*   Add function to group several elements into one
    
*   Add blackbox() function to generate box elements with arbitrary inputs
    
*   Allow element definition to specify label alignment
    
*   Added linestyle to element kwargs and definition
    
*   New elements:
    
    *   LED
        
    *   OPAMP\_NOSIGN
        
    *   GAP\_LABEL
        
    *   ELLIPSIS
        
    

v0.1.3, 21-Sep-2014

*   Added logic gate elements
    
*   Added transparent and dpi options to save() function
    
*   Fixed issues with zooming and rotating elements with arcs
    
*   LaTeX typesetting uses sans-serif, regular fonts for consistency
    

v0.1.0, 25-Aug-2014

*   Initial Release
    

Development[¶](#development "Link to this heading")
---------------------------------------------------

Report bugs and feature requests on the [Issue Tracker](https://github.com/cdelker/schemdraw/issues).

Code contributions are welcome, especially with new circuit elements (and we’d be happy to expand beyond electrical elements too). To contribute code, please fork the [source code repository](https://github.com/cdelker/schemdraw/) and issue a pull request. Make sure to include any new elements somewhere in the test Jupyter notebooks and in the documentation.

*   [Source Code](https://github.com/cdelker/schemdraw)
    

  

* * *

Want to support Schemdraw development? Need more circuit examples? Pick up the Schemdraw Examples Pack on buymeacoffee.com:

[![Buy Me A Coffee](https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png)](https://www.buymeacoffee.com/cdelker/e/55648)

* * *

Want to support Schemdraw development? Need more circuit examples? Pick up the Schemdraw Examples Pack on buymeacoffee.com:

[![Buy Me A Coffee](https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png)](https://www.buymeacoffee.com/cdelker/e/55648)
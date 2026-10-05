# Games Engines 1/eXtended Reality Assignment 2026

## Your design brief:

# The Soul Takes Birth, Takes Incarnation - To Learn
- Ram Dass 1931–2019

![Ram Dass](images/Fiorello-Ram-Dass-lead-1192561023.jpg)

- [A lovely song to inspire you](https://youtu.be/n4pHXsoE75s?si=LU5tkCowSNyi6_n3)

Your goal is to create an XR experience that a user can learn from. This can be music, storytelling, game design, programming, boolean logic, history, a language, how to tie a knot, how to make a cup of tea - whatever skill or knowledge you have - pass it on. Place the human learner at the center of the experience and teach them. Your design should be human created. You are free to work alone or as a team of up to 3.

You can use any of these projects as examples of XR interactions and workflows to start from, or start from an empty project:

| Project | What it demonstrates |
|---|---|
| [Quest:SDG](https://github.com/skooter500/questsdg) | A complete learning experience. Walk around a model of the TU Dublin campus and learn about the UN Sustainable Development Goals. Passthrough, hand tracking, Meta Scene SDK, spatial audio, voice over, UI in 3D space, importing models and a campus map |
| [Alien Hordz](https://github.com/skooter500/adrift) | An AR shooter that plays out in your own room. Meta Scene SDK scene anchors and spatial anchors, environment depth occlusion, hand pose detection, spawners, explosions and shaders |
| [Godó Hands](https://github.com/skooter500/hands) | A starter kit for holographic interactions. Hand tracking, the Hand Pose Detector, Godot OpenXR Vendors and Godot XR Tools all set up and ready to go |
| [Pop](https://github.com/skooter500/pop) | XR Tools pickables, a catapult, a playable instrument, physics balls and aliens |
| [xr26](https://github.com/skooter500/xr26) | This repo. All the examples we make in class this year - the tank game, the piano, passthrough, GPU particles, tweens and physics |
| [xrp25](https://github.com/skooter500/xrp25) | Last year's examples. The XR step sequencer, the tank game, room scanning and the spaceship that flies around your room |
| [Holograms](https://github.com/skooter500/holograms) | Motion captured musicians turned into holograms in Godot |

Technology you can use:

- [Godot OpenXR Vendors](https://github.com/GodotVR/godot_openxr_vendors) - passthrough, Meta Scene SDK, spatial anchors, hand tracking
- [Godot XR Tools](https://github.com/GodotVR/godot-xr-tools) - pickables, pointers, teleporting, UI
- [Hand Pose Detector](https://github.com/Malcolmnixon/GodotHandPoseDetector) - gestures
- Spatial audio, timers, tweens, physics, particles, shaders, AnimationPlayer, UI in 3D
- Any of the systems we learn on the course

Projects can be completed **individually or in teams of up to 3 students**.

## Proposal (10%)

Submit your proposal on Brightspace. Your proposal should include:

- Your project git repo URL
- Your idea in the README.MD in the repo. What will the learner learn? How will they learn it?
- What technology and interaction libraries you are using
- Who is on your team

## Submission Requirements

- Submit your project on Brightspace
- Git repo - Regular commits with human written messages
- Live demo on the Quest in class
- README.MD file with [all the sections in this template](assignmentreadme.md)
- YouTube video embedded in the README.MD file

## Weighting

| Category | Weighting |
|---|---|
| Proposal | 10% |
| Learning experience & interaction | 25% |
| Code & engine use | 25% |
| Look, sound & feel | 20% |
| Demo, documentation & project management | 20% |

## Rubric

Your grade is made up of five parts. Read each row and ask yourself "which box does my project fit in?". You do not need to hit every single thing in a category to get that grade. The A column is an outstanding project, *not a checklist*!

| | A | B | C | D | E |
|---|---|---|---|---|---|
| **Learning experience & interaction** | I put on the headset and I learn something new! The learner is at the center. There is a clear thing to learn, broken into steps that build on each other. The experience shows, lets the learner try, then checks they got it - with feedback, hints, scoring or progression. Lots of ways to interact: grab, point, press, gesture, speak, move around the room. Works in passthrough so the learner stays in their own space. Thoroughly tested with real a learners (maybe you!) and refined. | A clear learning goal with a few steps or levels and some feedback for the learner. Several kinds of interaction - buttons, pickables, hand gestures. Runs on the Quest. Tested on a few people. | A single thing to learn with one or two interactions. The learner can do something and something happens. May be one scene. Rough edges but it works and you can learn from it. | A Godot XR project that runs and responds to input, but there is not really a learning experience yet - no goal, no feedback, or mostly a starter example with little changed. | Nothing submitted, or the project does not open or crashes on start. |
| **Code & engine use** | Lots of your own GDScript organised into reusable scenes and scripts. Good use of Godot systems: signals, tweens, timers, physics, particles, shaders, AnimationPlayer, scene switching. Excellent use of OpenXR Vendors, XR Tools, hand tracking or the Meta Scene SDK. Code is readable with sensible names and some comments. Evidence of self directed learning. Can explain any line of it. Made a pull request to one of the starter repos and it was accepted. | Several scripts you wrote yourself. Uses signals and a couple of Godot systems (tweens, timers, physics, particles). Uses XR Tools or hand tracking. Splits the project into a few scenes. Code is mostly tidy and you can explain how it works. | A few scripts, mostly in one scene. Uses the basics from the labs (XR setup, transforms, input, collisions). Some copied code but you understand it. | Minimal self-written code. Mostly a lab example or a tutorial with small changes. Struggles to explain how it works. | No code, or code that does not run. |
| **Look, sound & feel** | Deployed to the Quest and it looks amazing. A clear visual style with original models, materials and UI. Spatial sound effects, voice over or music that you made or recorded. Juice: tweens, particles, glow, haptics and animation make every interaction feel good. Comfortable in XR - no sickness, text is readable, things are at the right scale and in reach. | Deployed to the Quest with a consistent look and mostly original assets. Sound on the main actions. Some tweens, particles or haptics to add feel. A few assets from online sources, credited. Minor glitches. | Runs on the Quest or on the XR simulator on PC. Simple models and primitives, some from online sources. Some sound. Little in the way of juice. | Default Godot look. Runs only in the editor, not tested on device. No sound, or inappropriate audio. Mostly downloaded assets. | No visuals or sound of your own. |
| **Demo, documentation & project management** | Clear initial proposal. Confident live demo: you put the headset on me, show the features, and talk about how you built it and what you learned. 30-40 commits, feature branches, commits all commented, and for teams an equal spread of commits. README has every section of the template: what it teaches, how to use it, how it works, what you built yourself, what you borrowed (with links) and a reflection on what you learned. Embedded, public, listed YouTube video that shows all the features. | Good live demo that shows the project working on the Quest and covers how you built it. 20-30 commits, one or two branches. All sections of the template filled out. Sources referenced. Minor gaps or issues with the video. | Demo happens but is rushed or not shown on the Quest. 10-20 commits, terse messages, no branches. Documentation present but missing sections, screenshots or the reflection. | Demo very brief or the project fails during it. Fewer than 10 commits, all in one day. Documentation is a few lines. No video. | No demo, no repo, or no documentation. |

### What the grades mean

- **A** - Outstanding. Went well beyond the brief. Someone genuinely learned something from it and you would be happy to put this on your portfolio as-is.
- **B** - Very good. Everything in the brief is done properly and the experience teaches what it says it teaches.
- **C** - Good. The brief is met. The project works, runs in XR and is your own.
- **D** - Pass. Something was submitted and runs, but a lot of the brief is missing.
- **E** - Fail. Nothing submitted, or it does not run.

### How to do well

- **Pick something you know.** Teach what you already understand. The best projects come from people passing on a skill they care about.
- **Get it on the headset early.** A tiny experience that runs on the Quest in week one. Add things to it every week.
- **Design for the learner** 
- **Make it yours.** Your own models, sounds and interactions. Original and simple beats copied and complex.
- **Show your work.** Take screenshots and record clips as you go. Keep dev notes. It makes the documentation and the video much easier.
- **Ask for help.** If you are stuck, ask in class or in the lab. I am a highly paid senior lecturer at your disposal every week!
- [Godot code of conduct applies](https://godotengine.org/code-of-conduct/)

## Examples of previous student work

- https://www.youtube.com/watch?v=FtxhKLheXAk&list=PL1n0B6z4e_E6cRfAfzaoXDueW38ZAFsI9
- https://www.youtube.com/watch?v=ZkrQnQmDK-M&list=PL1n0B6z4e_E6LmwpeGIW7vYhesNYUOLEN
- [2020-2021](https://youtube.com/playlist?list=PL1n0B6z4e_E5naCKOJDfU-sgX_3CdlRfN)
- [2019-2020](https://youtube.com/playlist?list=PL1n0B6z4e_E6GaGOHiBdPSW0QzICdGs4X)
- [2018-2019](https://youtube.com/playlist?list=PL1n0B6z4e_E5qaYwUOlJ63XI2OR9ty7Bs)

## Resources

- [Godot XR documentation](https://docs.godotengine.org/en/stable/tutorials/xr/)
- [Godot OpenXR Vendors manual](https://godotvr.github.io/godot_openxr_vendors/)
- [Meta Scene SDK in Godot](https://godotvr.github.io/godot_openxr_vendors/manual/meta/scene_manager.html)
- [Godot XR Tools](https://godotvr.github.io/godot-xr-tools/)
- [Godot Quick Reference](https://github.com/skooter500/csresources/blob/main/godot_ref.pdf)
- [Setting up Godot for Android](https://docs.godotengine.org/en/stable/tutorials/export/exporting_for_android.html)

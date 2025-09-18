<img width="400" height="300" alt="image" src="https://github.com/user-attachments/assets/9f2697a5-e736-4659-83e4-e2efbce93880"/>

# wirehead: prompt to pcb

**2nd place grand prize @ hackmit 2025 | [video demo](https://www.youtube.com/watch?v=HRUnMZR23MY)**

The world’s devices run on PCBs, but designing even simple PCBs can take dozens of hours of repetitive, effort-intensive work. As computer scientists, we work closely with electrical engineers (one of us is an electrical engineer!), so we’re no strangers to just how time-consuming PCB-design can be. A tool to speed up this process wouldn’t just help electrical engineers--anyone working with the hardware down the line, from mechanical engineers to computer scientists would feel the acceleration.

We tried to build a technical tool that doesn’t feel like a technical tool. It’s cute. It has an op-amp mascot. It’s designed to lower the (very high) barrier to entry to hardware design, while not dumbing things down for people who have years of experience in the field. It’s designed for people like us: makers and thinkers whose energy should be used for innovation, not reading datasheets.

## What it does

Wirehead is an end-to-end pipeline for designing PCBs. Our product takes in a list of components and automatically retrieves and processes their datasheets with a RAG pipeline. Then, Wirehead identifies the auxiliary components and layouts with MCP and generates a KiCAD netlist based on the adjacency graph of all the components. Using a combination of AI constraint generation and custom optimization metrics, Wirehead runs our CP-SAT packing algorithm on the netlist to find an optimal board layout, which is then fed back into KiCAD, where we generate the final PCB.

<img width="2571" height="1553" alt="image" src="https://github.com/user-attachments/assets/a308aec4-1b25-46c9-b345-482550959424" />

## How we built it

We leverage Claude Opus/Haiku, Cerebras Qwen235b, and DeepSeek through Tandemn to inject intelligent decision making and analysis into our system (in analysis of datasheets, internal decision making, and generation of adjacency lists). Our inference system has multiple backups to ensure robustness and zero single points of failure. We use state-of-the-art linear optimization software to power our layout engine, and our system is integrated with the open-source PCB design software KiCAD. Our dev team took full advantage of Windsurf’s agentic capabilities to write the requisite thousands of lines of code to push this project from idea to MVP in just one day. Wirehead uses a tech stack of Next.js/Tailwind/D3.js on the frontend and Flask/FastAPI on the backend to run the main and AI inference servers respectively.

## Individual Contributions

Jieruei built the frontend, schematic visualizations, KiCAD symbol indexing search, and server infrastructure. Allen built the LLM and KiCAD integrations to analyze datasheets, in order to determine auxiliary components, generate adjacency graphs, and create netlists. Alex designed the constrained linear programming algorithm for the layout engine. Ellie wrote the webscraping code to extract datasheets and information about electronic components (and also made the cute illustrations).

## Challenges we ran into

Going into this project, most of our team members had never designed a PCB before. We learned about component packages, datasheets, footprints, and schematics on the fly, and we also had to learn how to build for KiCAD, the open-source PCB design software we were using. KiCAD’s unique libraries and API were sometimes a challenge to understand without experience (for example, how did package correspond to footprint?), but by reading through all the resources we could find and  combining each teammate’s individual knowledge, we were able to build out a tool that interacts beautifully with KiCAD and understand much more about PCB design, a process integral to all the devices we use and depend on daily.

This was also a surprisingly technically difficult challenge. Datasheets, despite their supposed standardization, are anything but―our analysis needed to be smart enough to handle strange formats and different languages (many are in Chinese, for example) while also being efficient enough to read hundreds of pages of PDFs. The layout engine needs the intelligence of an AI with the optimality of an algorithmic solution, so we have a hybrid system where an LLM generates constraints for a CP-SAT linear programming solver that optimizes for component disjointness, board perimeter, and wire routing.

## Accomplishments that we're proud of

We are proud of just how many areas of CS and EE our project combines. We use LLMs to parse large amounts of data quickly while not being an LLM wrapper. We reframed PCBs and circuits into graphs, and created beautiful, responsive, and intuitive graph visualizations of how components and submodules interact with and are connected with each other. Our project also includes a novel CP-SAT algorithm that we developed to minimize the space needed to place components on the board. Finally, the overall project deals with a large issue in electrical engineering, so we were able to unite the fields of artificial intelligence, graph theory, theoretical computer science, and electrical engineering in one product in under 24 hours!

## What we learned

We were very lucky to have the opportunity to experiment with innovative new tools at HackMIT. For instance, using high-powered efficient LLM inference engines such as Claude Haiku and Cerebas Qwen235b to process PDFs and create adjacency lists was game-changing for our tool’s ability to quickly process large datasheets, one of the biggest bottlenecks in the PCB design process. Learning to use the Windsurf IDE also greatly sped up our development process with its code prediction and cursor prediction, which reduced the need to pore through APIs for the right piece of code. Throughout our project, we explored the intricacies of PCB design, an important skill for understanding and working with the hardware our electrical engineers develop.

## The route forward

Our project has a lot of potential to grow! We can see it as being an educational tool, a way to jump headfirst into designing PCBs without having to deeply understand all of the involved ins and outs of the process. With Education Mode on, Wirehead will include helpful details about the components being used, give tips on the various features of KiCAD, and describe the considerations Wirehead uses when placing and wiring components. By using this tool, budding electrical engineers can build intuition and real products at the same time, lowering the barrier to entry for the field.

As robotics and hardware fields grow, the demand for hardware developers will only increase, and our tool can accelerate the development process of cutting-edge companies and labs. But more than that, we can train the next generation of electrical engineers to ensure that these innovative fields continue to develop and evolve.

## Screenshots

<img width="2104" height="1128" alt="image" src="https://github.com/user-attachments/assets/7cea34d0-75ce-4d08-bacf-eee08367e54d" />

<img width="2102" height="1126" alt="image" src="https://github.com/user-attachments/assets/e871878b-f737-4af8-93ed-be430103c453" />

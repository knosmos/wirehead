"use client";
import React, { useState, useRef, useEffect } from "react";
import * as d3 from "d3";

export default function Build() {
  const [components, setComponents] = useState({
    "stm32f103": {
      name: "STM32",
      description: "Primary microcontroller unit (MCU) for processing and control.",
      img: "/component.jpg",
      submodules: {
        "220uF_capacitor": {
          name: "220uF Capacitor",
          description: "Stabilizes power supply to the MCU.",
          img: "/component.jpg",
        },
        "10k_resistor": {
          name: "10k Resistor",
          description: "Pull-up resistor for reset pin.",
          img: "/component.jpg",
        }
      }
    },
    "drv8825": {
      name: "DRV8825",
      description: "Step motor driver for controlling stepper motors.",
      img: "/component.jpg",
      submodules: {
        "100uF_capacitor": {
          name: "100uF Capacitor",
          description: "Filters voltage spikes from motor operation.",
          img: "/component.jpg",
        },
        "1k_resistor": {
          name: "1k Resistor",
          description: "Current limiting resistor for stepper motor coils.",
          img: "/component.jpg",
        }
      }
    }
  });
  const [adjGraph, setAdjGraph] = useState({
    "stm32f103": ["drv8825"],
    "r1": ["stm32f103"],
    "r2": ["stm32f103"],
    "r3": ["stm32f103"],
    "r4": ["stm32f103"],
    "drv8825": ["c1","c2","r5"],
    "c1": [],
    "c2": [],
    "r5": []
  });
  const graphRef = useRef(null);

  useEffect(() => {
    // Convert adjGraph to nodes and links
    type NodeType = { id: string; x?: number; y?: number; fx?: number | null; fy?: number | null };
    type LinkType = { source: string; target: string };
    const nodes: NodeType[] = Object.keys(adjGraph).map(id => ({ id }));
    const links: LinkType[] = Object.entries(adjGraph).flatMap(([source, targets]) =>
      targets.map(target => ({ source, target }))
    );

    const width = 400, height = 300;
    const svgEl = d3.select(graphRef.current)
      .attr("width", width)
      .attr("height", height)
      .style("background", "#f8fafc");

    // Remove previous graph content
    svgEl.selectAll("g").remove();
    svgEl.selectAll("text").remove();

    const simulation = d3.forceSimulation<NodeType>(nodes)
      .force("link", d3.forceLink<NodeType, LinkType>(links).id((d: NodeType) => d.id).distance(120))
      .force("charge", d3.forceManyBody().strength(-400))
      .force("center", d3.forceCenter(width / 2, height / 2));

    const link = svgEl.append("g")
      .attr("stroke", "#888")
      .attr("stroke-width", 2)
      .selectAll("line")
      .data(links)
      .enter().append("line");

    const node = svgEl.append("g")
      .attr("stroke", "#fff")
      .attr("stroke-width", 2)
      .selectAll("circle")
      .data(nodes)
      .enter().append("circle")
      .attr("r", 24)
      .attr("fill", "#054a22");
    (node as any).call(d3.drag()
      .on("start", function(event, d) {
        const node = d as NodeType;
        if (!event.active) simulation.alphaTarget(0.3).restart();
        node.fx = node.x;
        node.fy = node.y;
      })
      .on("drag", function(event, d) {
        const node = d as NodeType;
        node.fx = event.x;
        node.fy = event.y;
      })
      .on("end", function(event, d) {
        const node = d as NodeType;
        if (!event.active) simulation.alphaTarget(0);
        node.fx = null;
        node.fy = null;
      })
    );

    const label = svgEl.append("g")
      .selectAll("text")
      .data(nodes)
      .enter().append("text")
      .text((d: NodeType) => d.id)
      .attr("text-anchor", "middle")
      .attr("dy", ".35em")
      .attr("font-size", "0.5rem")
      .attr("fill", "#fff");

    simulation.on("tick", () => {
      link
        .attr("x1", (d: any) => ((d.source as NodeType).x ?? 0))
        .attr("y1", (d: any) => ((d.source as NodeType).y ?? 0))
        .attr("x2", (d: any) => ((d.target as NodeType).x ?? 0))
        .attr("y2", (d: any) => ((d.target as NodeType).y ?? 0));
      node
        .attr("cx", (d: NodeType) => d.x ?? 0)
        .attr("cy", (d: NodeType) => d.y ?? 0);
      label
        .attr("x", (d: NodeType) => d.x ?? 0)
        .attr("y", (d: NodeType) => d.y ?? 0);
    });
  }, [adjGraph]);
  return (
    <main className="flex min-h-screen flex-col items-center font-mono bg-gray-200">
      <div className="flex min-h-screen flex-col items-center p-10 w-full md:w-1/2">
        <h1 className="text-6xl font-bold my-5 font-serif">Wirehead</h1>
        <hr/>
        <div className="flex items-center border border-emerald-800 rounded-full px-4 py-2 mb-5 bg-green-300">
          <span className="w-2 h-2 rounded-full mr-5 bg-emerald-800 animate-ping"></span>
          <p className="uppercase tracking-widest font-mono text-emerald-800">status: reading datasheets...</p>
        </div>
        <h2 className="text-2xl font-bold my-5 font-mono">Component Selection</h2>
        <div className="w-full">
          {Object.entries(components).map(([key, comp]) => (
            <div key={key} className="mb-8">
              <div className="flex items-center mb-4">
                <img src={comp.img} alt={comp.name} className="w-24 h-24 mr-4 rounded-lg border"/>
                <div>
                  <h3 className="text-xl font-bold">{comp.name}</h3>
                  <p className="text-gray-600">{comp.description}</p>
                </div>
              </div>
              {comp.submodules && (
                <div className="ml-8 border-l-2 border-gray-300 pl-4">
                  {Object.entries(comp.submodules).map(([subKey, subComp]) => (
                    <div key={subKey} className="flex items-center mb-2">
                      <img src={subComp.img} alt={subComp.name} className="w-12 h-12 mr-4 rounded-lg border"/>
                      <div>
                        <h5 className="font-bold">{subComp.name}</h5>
                        <p className="text-gray-600">{subComp.description}</p>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          ))}
        </div>
        <hr/>
        <h2 className="text-2xl font-bold my-5 font-mono">Schematic Generation</h2>
        <div className="my-8 w-full">
          <h3 className="text-xl font-bold mb-2">Component Graph</h3>
          <svg ref={graphRef} className="border rounded shadow w-full" />
        </div>
        
        <h2 className="text-2xl font-bold my-5 font-mono">PCB Layout</h2>
      </div>
    </main>
  );
}
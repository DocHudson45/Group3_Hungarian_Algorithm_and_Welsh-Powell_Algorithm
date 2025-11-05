<div align="center">
    <h1>Graph Theory - EF234304 (2025)</h1>
</div>

<p align="center">
  <b>Institut Teknologi Sepuluh Nopember</b><br>
  Sepuluh Nopember Institute of Technology
</p>

<p align="center">
  <img src="assets/Badge_ITS.png" width="50%">
</p>
  
<p align="justify">Source code to <a href="https://www.its.ac.id/informatika/wp-content/uploads/sites/44/2023/11/Module-Handbook-Bachelor-of-Informatics-Program-ITS.pdf">Graph Theory (EF234304)</a>'s group assignment. All solutions were created by <a href="https://github.com/aleahfaa">Iffa Amalia Sabrina</a>, <a href="https://github.com/bellaacp">Bella Angeline Chong Puteri</a>, <a href="https://github.com/zan4yov">Razan Widya Reswara</a>, and <a href="https://github.com/DocHudson45">Muhammad Dzaky Radithya Ryrdi</a>.</p>

<div align="center">
  <table>
    <thead>
      <tr>
        <th align="center">NRP</th>
        <th align="center">Name</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td align="justify">5025221077</td>
        <td align="justify">Iffa Amalia Sabrina</td>
      </tr>
      <tr>
        <td align="justify">5025231073</td>
        <td align="justify">Bella Angeline Chong Puteri</td>
      </tr>
      <tr>
        <td align="justify">5025241004</td>
        <td align="justify">Razan Widya Reswara</td>
      </tr>
      <tr>
        <td align="justify">5025241010</td>
        <td align="justify">Muhammad Dzaky Radithya Ryrdi</td>
      </tr>
    </tbody>
  </table>
</div>

<p>On behalf of:<p>

<p><b>Ilham Gurat Adillion, S.Kom., M.Kom.</b></p>

<hr>


## Welsh-Powell Algorithm

**Purpose:** Assign colors
to graph nodes so that no two adjacent nodes share the same color (graph coloring). 

**How it works:**
1. Calculate degree for each node
2. Sort nodes in decreasing degree
3. Assign the first color to the highest-degree node, and all other non-adjacent nodes
4. Repeat with new colors until all nodes are colored

**Input example:**
```
Enter nodes: A, B, C, D, E
Enter edges as: u v cost
A B 10
B C 5
A D 7
C E 8
D E 3
B D 2
B E 4
```

**Output example:**
![gif](./assets/1A.gif)
<img width="191" height="369" alt="Screenshot 2025-11-05 at 19 28 46" src="https://github.com/user-attachments/assets/1e57889d-5448-432a-9279-68086bb24043" />


## Hungarian Algorithm
**Purpose:** To find the most efficient one-to-one assignment between two sets (e.g., workers <-> tasks) with the mininum total cost.

**What it does:** It matches items from Set A to Set B in the best possible way so the overall cost is as low as possible. 

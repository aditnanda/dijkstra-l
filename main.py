import webview


def main():
    # Embedded HTML content
    html_content = """
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <title>Dijkstra</title>
    <style>
        body {
            font-family: Arial, sans-serif;

            background-color: #f0f0f0;
        }

        #container {
            display: flex;
    flex-direction: column;
            text-align: center;
            padding: 20px;
            border: 1px solid #ccc;
            border-radius: 5px;
            background-color: #fff;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }

        .columns {
            display: flex;
            flex-wrap: wrap;
        }
        
        .column {
            flex: 1;
            padding: 10px;
        }
        
        canvas {
            border: 1px solid black;
            cursor: pointer;
            margin-top: 10px;
        }
        
        form {
            margin-bottom: 10px;
        }


        /* Gaya untuk modal */
        .modal {
            display: none;
            position: fixed;
            z-index: 1;
            left: 0;
            top: 0;
            width: 100%;
            height: 100%;
            overflow: auto;
            background-color: rgba(0, 0, 0, 0.4);
        }

        .modal-content {
            background-color: #fefefe;
            margin: 10% auto;
            padding: 20px;
            border: 1px solid #888;
            width: 30%;
            border-radius: 6px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }

        .modal-content-small {
            background-color: #fefefe;
            margin: 10% auto;
            padding: 20px;
            border: 1px solid #888;
            width: 20%;
            border-radius: 6px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }

        .modal-content-large {
            background-color: #fefefe;
            margin: 10% auto;
            padding: 20px;
            border: 1px solid #888;
            width: 50%;
            border-radius: 6px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }

        .close {
            color: #aaa;
            float: right;
            font-size: 28px;
            font-weight: bold;
        }

        .close:hover,
        .close:focus {
            color: black;
            text-decoration: none;
            cursor: pointer;
        }

    </style>
</head>

<body>

    <div id="container">
        <!-- <h1>Dijkstra</h1> -->
        
        <div class="columns">
            <div class="column">
                <canvas id="canvas" width="600" height="400"></canvas>
            </div>
            <div class="column">
                <div class="button-group">
                    <button onclick="setMode('edge')">Add Edge</button>
                    <button onclick="setMode('move')">Move Vertex</button>
                    <button onclick="addVertex()">Add Vertex</button>
                    <button onclick="removeVertex()">Delete Vertex</button>
        
                </div>
                <p><br></p>
                <form id="dijkstraForm">
                    <label for="startVertex">Start:</label>
                    <input type="number" id="startVertex" name="startVertex" value="1">
                    <label for="endVertex">End:</label>
                    <input type="number" id="endVertex" name="endVertex" value="3">
                    <button onclick="runDijkstra()" type="button">Run Dijkstra</button>
                </form>
                <br>
                <p id="hasilnya"></p>
            </div>
        </div>
    </div>

    <!-- Tambahkan modal -->
<div id="myModal" class="modal">
    <div class="modal-content">
      <span class="close">&times;</span>
      <p id="modalText"></p>
      <input type="text" id="modalInput" style="display: none;">
      <button id="modalButton" style="display: none;margin-top: 10px;">OK</button>
    </div>
  </div>

  <div id="myModal2" class="modal">
    <div class="modal-content-small">
        <div class="button-group">
            <button id="ubahButton" class="modal-button">Ubah</button>
            <button id="hapusButton" class="modal-button" style="background-color: red;">Hapus</button>
        </div>
    </div>
  </div>
  



  <script>

    let inputValue = null; // Variabel untuk menyimpan nilai yang diinput
  
    // Fungsi untuk menampilkan modal dengan pesan tertentu
    function showModal(message, input = false) {
      const modal = document.getElementById('myModal');
      const modalText = document.getElementById('modalText');
      const modalInput = document.getElementById('modalInput');
      const modalButton = document.getElementById('modalButton');
  
      modalText.textContent = message;
      if (input) {
        modalInput.style.display = 'block';
        modalButton.style.display = 'block';
      } else {
        modalInput.style.display = 'none';
        modalButton.style.display = 'none';
      }
  
      modal.style.display = 'block';
  
      // Aksi saat tombol OK pada modal ditekan
      modalButton.onclick = function() {
        const newValue = modalInput.value;
        if (newValue.trim() !== '') {
          inputValue = newValue; // Menyimpan nilai yang diinput
          modal.style.display = 'none';
        } else {
          showModal('Please insert a valid value.');
        }
      }
  
      // Aksi saat tombol close pada modal ditekan
      const spanClose = document.getElementsByClassName('close')[0];
      spanClose.onclick = function() {
        modal.style.display = 'none';
      }
  
      // Aksi saat pengguna mengklik area di luar modal (untuk menutup modal)
      window.onclick = function(event) {
        if (event.target === modal) {
          modal.style.display = 'none';
        }
      }
    }

    function showModal2(message, input = false) {
        const modal = document.getElementById('myModal2');

    
        modal.style.display = 'block';
    
    
        // Aksi saat tombol close pada modal ditekan
        const spanClose = document.getElementsByClassName('close')[0];
        spanClose.onclick = function() {
          modal.style.display = 'none';
        }
    
        // Aksi saat pengguna mengklik area di luar modal (untuk menutup modal)
        window.onclick = function(event) {
          if (event.target === modal) {
            modal.style.display = 'none';
          }
        }
      }
  
    // Fungsi untuk menampilkan dialog input dan mengembalikan nilai yang diinput
    function showInputDialog1(message, clickedEdgeIndex) {
        
        showInputDialog2('Insert new value for edge:', clickedEdgeIndex);
    
        
    }
    

    // Fungsi untuk menampilkan dialog input dan mengembalikan nilai yang diinput
    function showInputDialog2(message,clickedEdgeIndex) {
        document.getElementById('modalInput').value = null;
        showModal(message, true);
        const modalButton = document.getElementById('modalButton');
        modalButton.textContent = 'OK';
        modalButton.style.display = 'block';
        // Mengembalikan nilai yang diinput ketika modal ditutup
        return new Promise((resolve, reject) => {
          modalButton.onclick = function() {
            if (document.getElementById('modalInput').value !== null) {
                const newValue = document.getElementById('modalInput').value;
                if (newValue !== null && newValue.trim() !== '') {
                    vertices[clickedEdgeIndex.from].edgeValues[clickedEdgeIndex.to] = parseInt(newValue);
                    draw();
                    document.getElementById('myModal').style.display = 'none';
                }
            } else {
            }
          }
        });
      }

      // Fungsi untuk menampilkan dialog input dan mengembalikan nilai yang diinput
    function showInputDialog3(message,edgeStart,endVertex) {
        document.getElementById('modalInput').value = null;
        showModal(message, true);
        const modalButton = document.getElementById('modalButton');
        modalButton.textContent = 'OK';
        modalButton.style.display = 'block';
        // Mengembalikan nilai yang diinput ketika modal ditutup
        return new Promise((resolve, reject) => {
          modalButton.onclick = function() {
            if (document.getElementById('modalInput').value !== null) {
                const value = document.getElementById('modalInput').value;
                if (value !== null && value.trim() !== '') {
                    vertices[edgeStart].edges.push(endVertex);
                    vertices[edgeStart].edgeValues.push(parseInt(value));
                    draw();
                    document.getElementById('myModal').style.display = 'none';
                }
            } else {
              reject('Nilai Invalid.');
            }
          }
        });
      }
  
    // Di dalam kode Anda, gunakan fungsi showInputDialog untuk menampilkan modal dialog input
    // dan gunakan nilai yang dikembalikan (dengan menggunakan Promise) untuk melakukan sesuatu
    // dengan nilai yang diinput, seperti mengubah nilai edge atau melakukan tindakan lainnya.
  </script>
  
    <script>
        const canvas = document.getElementById('canvas');
        const ctx = canvas.getContext('2d');
        let vertexCount = 3;
        let vertices = [];
        let mode = 'move';
        let dragging = false;
        let selectedVertex = null;
        let edgeStart = null;
        let deleteEdgeTimeout = null;

        function resetCanvas() {
            vertices = []; // Menghapus semua vertices
            draw(); // Menggambar kembali canvas yang kosong
        }



        function clearCanvas() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
        }

        function drawVertex(x, y, label) {
            ctx.beginPath();
            ctx.arc(x, y, 12, 0, Math.PI * 2); // Ubah ukuran vertex menjadi 12
            ctx.fillStyle = 'green';
            ctx.fill();
            ctx.closePath();
            ctx.font = 'bold 14px Arial'; // Tambahkan "bold" untuk label vertex
            ctx.fillStyle = 'white';
            ctx.fillText(label, x - 6, y + 5); // Beri padding untuk label
        }

        function drawEdge(startX, startY, endX, endY, value) {
            ctx.beginPath();
            ctx.moveTo(startX, startY);
            ctx.lineTo(endX, endY);
            ctx.strokeStyle = 'black';
            ctx.stroke();
            if (value !== undefined) {
                ctx.font = '14px Arial';
                ctx.fillStyle = 'black';
                ctx.fillText(value, (startX + endX) / 2, (startY + endY) / 2);
            }
            ctx.closePath();
        }

        function draw() {
            clearCanvas();
            for (let i = 0; i < vertices.length; i++) {
                for (let j = 0; j < vertices[i].edges.length; j++) {
                    const endVertex = vertices[vertices[i].edges[j]];
                    drawEdge(
                        vertices[i].x,
                        vertices[i].y,
                        endVertex.x,
                        endVertex.y,
                        vertices[i].edgeValues[j]
                    );
                }
            }
            for (let i = 0; i < vertices.length; i++) {
                const label = drawNextVertexLabel(i+1);
                drawVertex(vertices[i].x, vertices[i].y, label);
            }
            if (edgeStart !== null && mode === 'edge') {
                const {
                    x,
                    y
                } = getCursorPosition(event);
                drawEdge(vertices[edgeStart].x, vertices[edgeStart].y, x, y);
            }
        }


        function getRandomPosition() {
            const x = Math.floor(Math.random() * (canvas.width - 20)) + 10;
            const y = Math.floor(Math.random() * (canvas.height - 20)) + 10;
            return {
                x,
                y
            };
        }

        function addVertex() {
            const {
                x,
                y
            } = getRandomPosition();
            vertices.push({
                x,
                y,
                edges: [],
                edgeValues: []
            });
            draw();
        }

        function getCursorPosition(event) {
            const rect = canvas.getBoundingClientRect();
            const x = event.clientX - rect.left;
            const y = event.clientY - rect.top;
            return {
                x,
                y
            };
        }

        function checkClickedVertex(cursorX, cursorY) {
            for (let i = 0; i < vertices.length; i++) {
                const distance = Math.sqrt((cursorX - vertices[i].x) ** 2 + (cursorY - vertices[i].y) ** 2);
                if (distance <= 8) {
                    return i;
                }
            }
            return null;
        }

        canvas.addEventListener('mousedown', function(event) {
            const {
                x,
                y
            } = getCursorPosition(event);
            selectedVertex = checkClickedVertex(x, y);
            if (selectedVertex !== null && mode === 'move') {
                dragging = true;
            } else if (mode === 'edge') {
                edgeStart = checkClickedVertex(x, y);
            } else {
                // Jika mode bukan 'move' atau 'edge', maka cek apakah klik dilakukan di atas edge
                const clickedEdgeIndex = checkClickedEdge(x, y);
                if (clickedEdgeIndex !== null) {
                    showInputDialog1('Pilih:',clickedEdgeIndex);
                    
                }
            }
        });

        canvas.addEventListener('mousemove', function(event) {
            if (dragging && selectedVertex !== null && mode === 'move') {
                const {
                    x,
                    y
                } = getCursorPosition(event);
                vertices[selectedVertex].x = x;
                vertices[selectedVertex].y = y;
                draw();
            } else if (edgeStart !== null && mode === 'edge') {
                draw();
            }
        });

        canvas.addEventListener('mouseup', function(event) {
            if (dragging && selectedVertex !== null && mode === 'move') {
                dragging = false;
                selectedVertex = null;
            } else if (edgeStart !== null && mode === 'edge') {
                const {
                    x,
                    y
                } = getCursorPosition(event);
                const endVertex = checkClickedVertex(x, y);

                // Mencegah menghubungkan indeks yang lebih tinggi ke indeks yang lebih rendah
                if (endVertex !== null && edgeStart !== endVertex && endVertex > edgeStart) {
                    showInputDialog3('Insert edge value:',edgeStart,endVertex);
                    
                }
                edgeStart = null;
            }
        });


        function checkClickedEdge(cursorX, cursorY) {
            for (let i = 0; i < vertices.length; i++) {
                for (let j = 0; j < vertices[i].edges.length; j++) {
                    const startX = vertices[i].x;
                    const startY = vertices[i].y;
                    const endVertex = vertices[vertices[i].edges[j]];
                    const endX = endVertex.x;
                    const endY = endVertex.y;

                    // Calculate distance from point to line (edge)
                    const distance = Math.abs((endY - startY) * cursorX - (endX - startX) * cursorY + endX * startY - endY *
                            startX) /
                        Math.sqrt((endY - startY) ** 2 + (endX - startX) ** 2);

                    // If the distance is within a threshold (e.g., 5 pixels), consider it a click on the edge
                    if (distance <= 5) {
                        return {
                            from: i,
                            to: j
                        }; // Return the indices of the edge clicked
                    }
                }
            }
            return null;
        }

        function getRandomEdges(vertexCount, currentIndex) {
            const edges = [];
            const edgeValues = [];
            const connected = {}; // Menyimpan vertex yang sudah terhubung

            for (let i = currentIndex + 1; i < vertexCount; i++) {
                edges.push(i);
                edgeValues.push(Math.floor(Math.random() * 10) + 1); // Nilai edge acak dari 1 hingga 10
                connected[i] = true;
                connected[currentIndex] = true; // Tandai kedua vertex terhubung
            }
            return {
                edges,
                edgeValues
            };
        }



        function setMode(selectedMode) {
            mode = selectedMode;
            edgeStart = null;
        }

        function getNextLabel(index) {
            return index.toString();
        }

        function drawNextVertexLabel(index) {
            const label = getNextLabel(index);
            return label;
        }

        function removeVertex() {
            if (vertices.length === 0) {
                return;
            }

            vertices.pop();
            for (let i = 0; i < vertices.length; i++) {
                for (let j = vertices[i].edges.length - 1; j >= 0; j--) {
                    if (vertices[i].edges[j] >= vertices.length) {
                        vertices[i].edges.splice(j, 1);
                        vertices[i].edgeValues.splice(j, 1);
                    }
                }
            }
            draw();
        }


        function runDijkstra() {
            const INF = Number.MAX_SAFE_INTEGER;
            const distance = [];
            const visited = [];
            const parent = [];
            let allPaths = [];
            let dijkstraSteps = [];

            const ver_edge = getDataFromCanvas();
            const nodes = ver_edge.nodes;
            const edges = ver_edge.edges;

            if (nodes.length === 0 || edges.length === 0) {
                showModal('Tidak ada vertex atau edge yang tersedia. Silakan tambahkan vertex dan edge terlebih dahulu.');
                return;
            }

            for (let i = 0; i < nodes.length; i++) {
                distance[i] = INF;
                visited[i] = false;
                parent[i] = -1;
            }



            const startNode = parseInt(document.getElementById('startVertex').value)-1;
            const endNode = parseInt(document.getElementById('endVertex').value)-1;

            if (endNode > nodes.length-1 || startNode < 0) {
                showModal('Vertex Awal tidak boleh kurang dari 0 atau Vertex Akhir tidak boleh lebih dari jumlah Vertex.');
                return;
            }

            distance[startNode] = 0;

            function findAllPaths(currentNode, currentPath, currentPathValue) {
                visited[currentNode] = true;
                currentPath.push(currentNode);

                if (currentNode === endNode) {
                    allPaths.push({
                        path: [...currentPath],
                        totalValue: currentPathValue
                    });
                } else {
                    for (let v = 0; v < nodes.length; v++) {
                        if (!visited[v] && edges.some(edge => (edge.source === currentNode && edge.target === v) || (edge.source === v && edge.target === currentNode))) {
                            const edgeIndex = edges.findIndex(edge => (edge.source === currentNode && edge.target === v) || (edge.source === v && edge.target === currentNode));
                            const edgeValue = edges[edgeIndex].weight;

                            findAllPaths(v, currentPath, currentPathValue + edgeValue);
                        }
                    }
                }

                visited[currentNode] = false;
                currentPath.pop();
            }

            findAllPaths(startNode, [], 0);

            displayPathsAndTotalValues(allPaths);

            for (let count = 0; count < nodes.length - 1; count++) {
                let u = -1;
                for (let i = 0; i < nodes.length; i++) {
                    if (!visited[i] && (u === -1 || distance[i] < distance[u])) {
                        u = i;
                    }
                }

                visited[u] = true;

                for (let v = 0; v < nodes.length; v++) {
                    if (!visited[v] && edges.some(edge => (edge.source === u && edge.target === v) || (edge.source === v && edge.target === u))) {
                        const edgeIndex = edges.findIndex(edge => (edge.source === u && edge.target === v) || (edge.source === v && edge.target === u));
                        const weight = edges[edgeIndex].weight;
                        if (distance[u] !== INF && distance[u] + weight < distance[v]) {
                            distance[v] = distance[u] + weight;
                            parent[v] = u;
                        }
                    }
                }
            }

            // Menyorot jalur terpendek pada tampilan graf
            draw();
            let path = [];
            for (let j = endNode; j !== -1; j = parent[j]) {
                path.push(j);
            }
            path.reverse();

            // Highlight the shortest path by changing the color of the lines on that path
            ctx.strokeStyle = 'red';
            ctx.lineWidth = 3;
            for (let k = 0; k < path.length - 1; k++) {
                const node1 = path[k];
                const node2 = path[k + 1];
                const edge = edges.find(e =>
                    (e.source === node1 && e.target === node2) || (e.source === node2 && e.target === node1)
                );
                const weight = edge ? edge.weight : ''; // Get weight from edge object
                ctx.beginPath();
                ctx.moveTo(nodes[node1].x, nodes[node1].y);
                ctx.lineTo(nodes[node2].x, nodes[node2].y);
                ctx.stroke();
                ctx.font = '14px Arial';
                ctx.fillStyle = 'black';
                ctx.fillText(weight, (nodes[node1].x + nodes[node2].x) / 2, (nodes[node1].y + nodes[node2].y) / 2);
            }


        }

        function displayPathsAndTotalValues(paths) {
            outTemp = [];
            paths.forEach((path, index) => {
                outTemp.push({
                    'path' : `${path.path.map(node => node +1).join(' -> ')}</br>Nilai = ${path.totalValue}</br></br>`,
                    'edge_value' : path.totalValue
                })
            });
            let smallestEdgeValue = Infinity;
            let objectWithSmallestEdgeValue = null;

            for (let i = 0; i < outTemp.length; i++) {
                if (outTemp[i].edge_value < smallestEdgeValue) {
                    smallestEdgeValue = outTemp[i].edge_value;
                    objectWithSmallestEdgeValue = outTemp[i];
                }
            }

            console.log('Object dengan edge_value terkecil:', objectWithSmallestEdgeValue);
            console.log('Log PerhitunganL', outTemp);

            const myParagraph = document.getElementById('hasilnya');

            // Mengubah isi elemen <p> menggunakan innerHTML
            myParagraph.innerHTML = objectWithSmallestEdgeValue.path;

            try{
                pywebview.api.sendEdgeValue({
                    hasil:objectWithSmallestEdgeValue.path
                });
            }catch(e){
            
            }
        }

        function getDataFromCanvas() {
            const nodes = [];
            const edges = [];

            // Mengambil data posisi vertex dari vertices
            for (let i = 0; i < vertices.length; i++) {
                const node = {
                    id: i,
                    x: vertices[i].x,
                    y: vertices[i].y,
                    edges: []
                };
                nodes.push(node);

                // Mengambil data hubungan antar vertex dan bobot edge-nya dari edges
                for (let j = 0; j < vertices[i].edges.length; j++) {
                    const edge = {
                        source: i, // nodeIndex1
                        target: vertices[i].edges[j], // nodeIndex2
                        weight: vertices[i].edgeValues[j] // weight
                    };
                    node.edges.push(edge);
                    edges.push(edge);
                }
            }

            // Output hasil ekstraksi data dari canvas
            console.log("Nodes:");
            console.log(nodes);
            console.log("Edges:");
            console.log(edges);

            const data = JSON.stringify({
                nodes,
                edges
            }); // Mendapatkan data dari canvas dalam bentuk string JSON
            // Menggunakan pywebview API untuk mengirim data ke Python

            // Jika Anda ingin mengembalikan data untuk digunakan di tempat lain, dapat menggunakan return
            return {
                nodes,
                edges
            };
        }

        // Panggil fungsi getDataFromCanvas untuk mendapatkan data dari canvas

        draw();
    </script>

</body>

</html>

    """

    # Membuat jendela webview dan memuat file HTML
    webview.create_window('Dijkstra', html=html_content,width=900, height=550)
    webview.start()

if __name__ == '__main__':
    main()


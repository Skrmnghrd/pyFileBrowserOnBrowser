		$(function() {
			  $('a#process_input').bind('click', function() {
				$.getJSON('{{url_for("_back_")}}', {

				}, function(data) 
				{
					var clear_us = ['directories','files', 'current_dir'];
					clear_us.map( function(item) 
					{
						var clear_me = document.getElementById(item);
						while (clear_me.firstChild) {
							clear_me.removeChild(clear_me.firstChild);
						}
					});

					for (var keys in data)
					{
          var test = data[keys]
					
					document.getElementById("current_dir").innerHTML = test['current_dir'];
          test['dirs_in_cwd'].map( function(item)
						{
            var btn = document.createElement("BUTTON");
            var textnode = document.createTextNode(item);
            btn.appendChild(textnode);
						btn.value = item;
						btn.onclick = function(){ButtonDirChange(this)};
            document.getElementById("directories").appendChild(btn);
         		});
				

					test['files_in_cwd'].map( function(item)
						{
            var node_files = document.createElement('a');
            var textnode = document.createTextNode(item);
            node_files.appendChild(textnode);
						node_files.title = item;
						node_files.href = Flask.url_for("_get_file", {"file_name": item})
            document.getElementById("files").appendChild(node_files);
          	});
						
						};
			
				});
				return false;
			  });
			});
			//end of _back

      $.getJSON('_first_open', function(data){
        for (var keys in data){
          var test = data[keys]
          

          document.getElementById("current_dir").innerHTML = test['current_dir'];
          test['dirs_in_cwd'].map( function(item){
            var btn = document.createElement("BUTTON");
            var textnode = document.createTextNode(item);
            btn.appendChild(textnode);
						btn.value = item;
						btn.onclick = function(){ButtonDirChange(this)};
            document.getElementById("directories").appendChild(btn);
          });

          test['files_in_cwd'].map( function(item){
            var node_files = document.createElement('a');
            var textnode = document.createTextNode(item);
						node_files.appendChild(textnode);
						node_files.title = item;
						node_files.href = Flask.url_for("_get_file", {"file_name": item});
            
            document.getElementById("files").appendChild(node_files);
          });
          
          
        };

      });
			//end of first open
			function ButtonDirChange(elem)
			{
				$.getJSON('{{url_for("_change_dir")}}',
				{
					directory: elem.value
				}, function(data){
					
					var clear_us = ['directories','files', 'current_dir'];
					clear_us.map( function(item) 
					{
						var clear_me = document.getElementById(item);
						while (clear_me.firstChild) 
						{
							clear_me.removeChild(clear_me.firstChild);
						}

					});

					for (var keys in data)
					{
          var test = data[keys]
					
					document.getElementById("current_dir").innerHTML = test['current_dir'];
          test['dirs_in_cwd'].map( function(item)
						{
            var btn = document.createElement("BUTTON");
            var textnode = document.createTextNode(item);
            btn.appendChild(textnode);
						btn.value = item;
						btn.onclick = function(){ButtonDirChange(this)};
            document.getElementById("directories").appendChild(btn);
         		});
				

					test['files_in_cwd'].map( function(item)
						{
            var node_files = document.createElement('a');
            var textnode = document.createTextNode(item);
            node_files.appendChild(textnode);
						node_files.title = item;
						node_files.class = "btn btn-default";
						node_files.href = Flask.url_for("_get_file", {"file_name": item});
						node_files.onclick = function(){DownloadThis(this)};
            document.getElementById("files").appendChild(node_files);
          	});

						};
				});
			};
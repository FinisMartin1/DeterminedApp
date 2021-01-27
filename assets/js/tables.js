function createRow(tableName) {
    $('#' + tableName).append(`
    <tr class="course">
        <td><input placeholder="New" name="CourseNum" class="courses"
            style="width:45px" min="1000" max="9999" type="number"
            required /></td>
        <td><input placeholder="New" name="DeptId" class="courses"
            style="width:60px" required pattern="[A-Za-z]{4}" maxlength="4"
            oninvalid="this.setCustomValidity('Must be 4 characters')"
            onchange="this.setCustomValidity('')" />
        </td>
        <td><textarea placeholder="New" name="Title" cols="18" rows="2"
            maxlength="100" required></textarea></td>
        <td><input placeholder="New" name="Fname" class="courses"
            style="width:80px" required pattern="[A-Za-z]+" maxlength="35"
            oninvalid="this.setCustomValidity('Names can only be made of characters')"
            onchange="this.setCustomValidity('')" />
        </td>
        <td><input placeholder="New" name="Lname" class="courses"
            style="width:80px" required pattern="[A-Za-z]+" maxlength="35"
            oninvalid="this.setCustomValidity('Names can only be made of characters')"
            onchange="this.setCustomValidity('')" />
        </td>
        <td><textarea placeholder="New" name="SWP" cols="18" rows="2"
            required></textarea></td>
        <td><input placeholder="New" name="Term" class="courses"
            style="width:65px" required maxlength="6"
            pattern="[sS][pP][rR][iI][nN][gG]|[sS][uU][mM][mM][eE][rR]|[fF][aA][lL][lL]"
            oninvalid="this.setCustomValidity('Please use Fall, Spring, or Summer')"
            onchange="this.setCustomValidity('')" />
        </td>
        <td><input placeholder="New" name="Year" class="courses"
            style="width:45px" required min="1000" max="9999"
            type="number" /></td>
        <td><button type="Button" onclick="deleterow('courseDataTable', this)"
            class="btn btn-outline-danger btn-sm"
            style="border:none;">X</button>
    </tr>
    `);
}

function createSwpRow(tableName, product, course_id, dept_id, terms) {
    if (course_id == "All"){course_id=""; }
    else{course_id = Number(course_id.substr(0,4));}
    if (product == "All"){product=""; }
    if (dept_id == "All"){dept_id=""; }
    else {dept_id = "value=".concat(dept_id)}
    if (terms == "All"){var term = year =""}
    else{
        var terms_array = terms.split(" ")
        var term = "value=".concat(terms_array[0]);
        var year = "value=".concat(terms_array[1]);
    }
    

    $('#' + tableName).append(`
    <tr>
        <td style="display:none;"><input value="None" name="RowId" style="display:none;" >
        <td><textarea cols="8" rows="1" name="Product" placeholder="New"
                required >${product}</textarea></td>
        <td><input value=${course_id} placeholder="New" name="CourseId" class="courses"
                style="width:45px" min="1000" max="9999" type="number"
                required /></td>
        <td><input ${dept_id} placeholder="New" name="DeptId" class="courses"
                style="width:60px" required pattern="[A-Za-z]{4}" maxlength="4"
                oninvalid="this.setCustomValidity('Must be 4 characters')"
                onchange="this.setCustomValidity('')" />
        </td>
        <td><input placeholder="New" name="Fname" ,
                class="courses" style="width:80px" required pattern="[A-Za-z]+"
                maxlength="35"
                oninvalid="this.setCustomValidity('Names can only be made of characters')"
                onchange="this.setCustomValidity('')" />
        </td>
        <td><input placeholder="New" name="Lname" ,
                class="courses" style="width:80px" required pattern="[A-Za-z]+"
                maxlength="35"
                oninvalid="this.setCustomValidity('Names can only be made of characters')"
                onchange="this.setCustomValidity('')" />
        </td>
        <td><input placeholder="New" name="Outcome"
                class="courses" style="width:45px" min="0" max="4" type="number"
                required /></td>
        <td><input placeholder="New" name="Score" class="courses"
                style="width:45px" min="0" max="100" type="number" required />
        </td>
        <td><input placeholder="New" ${term}  name="Term" , class="courses"
                style="width:65px" required maxlength="6"
                pattern="[sS][pP][rR][iI][nN][gG]|[sS][uU][mM][mM][eE][rR]|[fF][aA][lL][lL]"
                oninvalid="this.setCustomValidity('Please use Fall, Spring, or Summer')"
                onchange="this.setCustomValidity('')" />
        </td>
        <td><input placeholder="New" ${year} name="Year" , class="courses"
                style="width:45px" required min="1000" max="9999"
                type="number" /></td>
        <td><button type="Button" onclick="deleterow('student_work_product_table', this)"
                class="btn btn-outline-danger btn-sm"
                style="border:none;">X</button></td>
    </tr>   
    `);
}

function deleterow(tableName, row) {
    var table = document.getElementById(tableName);
    var index = row.parentElement.parentElement.rowIndex
    table.deleteRow(index);
}

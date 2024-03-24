import os
import re

import inflection


def generate_service_file(dto_file_path, output_file_path, modelName):
    collection_name = modelName
    service_name = collection_name + 'Service'

    # Extract class name from the DTO file
    with open(dto_file_path, 'r') as file:
        dto_content = file.read()
        class_name_match = re.search(r'export class (\w+)', dto_content)

        if not class_name_match:
            raise ValueError("Cannot find a class definition in the DTO file")

        class_name = class_name_match.group(1)

        # Define the TypeScript service code template
        service_template = f"""
    import {{ Injectable, NotFoundException }} from '@nestjs/common';
    import * as admin from 'firebase-admin';
    import {{ {class_name} }} from './{os.path.basename(dto_file_path)[:-3]}';

    @Injectable()
    export class {service_name} {{
        private db: admin.firestore.Firestore;
        private projectCollection: admin.firestore.CollectionReference;

        constructor() {{
            this.db = admin.firestore();
            this.projectCollection = this.db.collection('{collection_name}');
        }}

        async set(create{class_name}Dto: {class_name}): Promise<void> {{
            await this.projectCollection.doc(create{class_name}Dto.id).set(create{class_name}Dto);
        }}

        async remove(uid: string): Promise<void> {{
            await this.projectCollection.doc(uid).delete();
        }}

        async query(filter?: Record<string, any> | string): Promise<{class_name}[]> {{
            if (typeof filter === 'string') {{
                try {{
                    filter = JSON.parse(filter);
                }} catch (e) {{
                    console.error('Error parsing filter string as JSON:', e.message);
                    throw new Error('Invalid filter format. Expected an object or a JSON string.');
                }}
            }}

            if (!filter || Object.keys(filter).length === 0) {{
                console.error('Error: Query filter is either absent or empty');
                throw new Error('Error: Query is not correct');
            }}

            console.debug(`Initiating query with filter: ${{JSON.stringify(filter)}}`);

            let _query: FirebaseFirestore.Query = this.projectCollection;

            if (typeof filter === 'object') {{
                Object.entries(filter).forEach(([key, value]) => {{
                    console.debug(`Applying filter - Key: ${{key}}, Value: ${{JSON.stringify(value)}}`);
                    _query = _query.where(key, '==', value);
                }});
            }} else {{
                console.error('Error: Filter is not an object after parsing attempt.');
                throw new Error('Error: Query is not correct - filter is not an object.');
            }}

            try {{
                console.debug(`Final Query path: ${{_query}}`);

                const result = await _query.get();

                console.info(`Query successful. Retrieved ${{result.docs.length}} documents.`);
                console.info(`Query successful. The query was: ${{JSON.stringify(result.query)}}`);

                const parsedList: {class_name}[] = result.docs.map(doc => doc.data() as {class_name});
                console.debug(`Parsed documents: ${{JSON.stringify(parsedList)}}`);

                return parsedList;
            }} catch (error) {{
                console.error('Error during Firestore query execution:', error.message);
                throw new Error(`Error during Firestore query execution: ${{error.message}}`);
            }}
        }}

        async read(uid: string): Promise<{class_name}> {{
            const doc = await this.projectCollection.doc(uid).get();

            if (!doc.exists) {{
                throw new NotFoundException('{collection_name} not found');
            }}

            const project = doc.data() as {class_name};
            return project;
        }}
    }}
    """
    os.makedirs(os.path.dirname(output_file_path), exist_ok=True)

    # Write the generated service code to a TypeScript file
    with open(output_file_path, 'w') as file:
        file.write(service_template)


def generate_controller_file(service_file_path, dto_file_path, output_file_path, controller_name):
    with open(dto_file_path, 'r') as file:
        dto_content = file.read()
        class_name_match = re.search(r'export class (\w+)', dto_content)

        if not class_name_match:
            raise ValueError("Cannot find a class definition in the DTO file")

        class_name = class_name_match.group(1)

    # Extract service name from the service file
    with open(service_file_path, 'r') as file:
        service_content = file.read()
        service_name_match = re.search(r'export class (\w+)', service_content)

        if not service_name_match:
            raise ValueError("Cannot find a class definition in the service file")

        service_name = service_name_match.group(1)

    # Define the TypeScript controller code template
    controller_template = f"""
import {{
    Controller,
    Post,
    Delete,
    Get,
    Body,
    Param,
    Query,
    NotFoundException,
    UseGuards,
}} from '@nestjs/common';
import {{ {service_name} }} from './{os.path.basename(service_file_path)[:-3]}';
import {{ {class_name} }} from './{os.path.basename(dto_file_path)[:-3]}';
import {{ FirebaseAuthGuard }} from 'src/guards/firebase_auth.guard';
import {{ ApiTags, ApiOperation, ApiParam, ApiQuery }} from '@nestjs/swagger';

@UseGuards(FirebaseAuthGuard)
@ApiTags('{controller_name}')
@Controller('{inflection.camelize(controller_name, False)}')
export class {controller_name}Controller {{
    constructor(private readonly {service_name[0].lower() + service_name[1:]}: {service_name}) {{ }}

    @Post('set')
    @ApiOperation({{
        summary: 'Set (Create/Update) {controller_name}',
        description: 'Create or update a {controller_name.lower()} and store it in the database.',
    }})
    async set(@Body() {class_name[0].lower() + class_name[1:]}: {class_name}): Promise<void> {{
        await this.{service_name[0].lower() + service_name[1:]}.set({class_name[0].lower() + class_name[1:]});
    }}

    @Delete('delete/:uid')
    @ApiOperation({{
        summary: 'Delete {controller_name}',
        description: 'Delete a {controller_name.lower()} from the database based on UID.',
    }})
    @ApiParam({{ name: 'uid', description: 'UID of the {controller_name.lower()} to delete' }})
    async delete(@Param('uid') uid: string): Promise<void> {{
        if (!uid) {{
            throw new NotFoundException('UID is required');
        }}
        await this.{service_name[0].lower() + service_name[1:]}.remove(uid);
    }}

    @Get('query')
    @ApiOperation({{
        summary: 'Query {controller_name}s',
        description: 'Query the database for {controller_name.lower()}s using a dynamic map.',
    }})
    @ApiQuery({{ name: 'uid', required: true, description: 'User UID' }})
    @ApiQuery({{ name: 'filter', required: false, description: 'Dynamic query map' }})

    async query(
        @Query('filter') filter?: Record<string, any>
    ): Promise<{class_name}[]> {{

        return await this.{service_name[0].lower() + service_name[1:]}.query(filter);
    }}

    @Get(':uid')
    @ApiOperation({{
        summary: 'Read {controller_name}',
        description: 'Retrieve a {controller_name.lower()} from the database by UID.',
    }})
    @ApiParam({{ name: 'uid', description: 'UID of the {controller_name.lower()} to retrieve' }})
    async read(@Param('uid') uid: string): Promise<{class_name}> {{
        if (!uid) {{
            throw new NotFoundException('UID is required');
        }}
        const {controller_name.lower()} = await this.{service_name[0].lower() + service_name[1:]}.read(uid);
        if (!{controller_name.lower()}) {{
            throw new NotFoundException('{controller_name} not found');
        }}
        return {controller_name.lower()};
    }}
}}
"""
    # Ensure the directory exists before trying to write to it
    os.makedirs(os.path.dirname(output_file_path), exist_ok=True)

    # Write the generated controller code to a TypeScript file
    with open(output_file_path, 'w') as file:
        file.write(controller_template)

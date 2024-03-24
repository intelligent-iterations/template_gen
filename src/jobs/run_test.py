import os
from src.services.file_service import read_file, save_file
from src.jobs.create_model import createModel
from src.jobs.enchance_model import enhanceModel
# from jobs.test_model import testModel
# from jobs.model_to_service import modelToService
# from jobs.model_to_repository import modelToRepository

def runTest():
    print("Testing basic functions")
    
    workingPath = os.getcwd()
    
    tempPath = f'{workingPath}/temp/'
    className = 'Jose'
    pathName = 'jose.dart'
    
    modelPath = createModel(className, workingPath)    
    print(f'model created in {modelPath}')
    
    save_file(modelPath, primitiveClass)
    
    enhanceModel(modelPath)
    
    readEnchancedModelResult = read_file(modelPath).strip()
    
    expectation = readEnchancedModelResult == primitiveClassEnhanced.strip()
    
    if(expectation != True):
      print(f"Expection occured")
      print(f'readEnchancedModelResult should have been: {primitiveClassEnhanced}')
      print(f'instead is {readEnchancedModelResult}')
      print(f"Test finished with {expectation}")
    else:
      print('Success expectations are met')
    
 
 
primitiveClass = """
class Jose{
    String id;
    Jose2 jose2;            
}

class Jose2{
    String id
}   
"""    
primitiveClassEnhanced = """
import 'package:equatable/equatable.dart';

class Jose extends Equatable {
  Jose({required this.id, required this.jose2});

  final String? id;
  final Jose2? jose2;

  @override
  List<Object?> get props => [id, jose2];

  Map<String, dynamic> toJson() {
    return {'id': id, 'jose2': jose2?.toJson()};
  }

  factory Jose.fromJson(Map<String, dynamic> map) {
    return Jose(id: map['id'], jose2: Jose2.fromJson(map['jose2']??{}));
  }

  Jose copyWith({String? id, Jose2? jose2}) {
    return Jose(id: id ?? this.id, jose2: jose2 ?? this.jose2);
  }

 static Map<String, dynamic> exampleJson() {
    return {'id': "", 'jose2': Jose2.exampleJson()};
  }
}

class Jose2 extends Equatable {
  Jose2({required this.id});

  final String? id;

  @override
  List<Object?> get props => [id];

  Map<String, dynamic> toJson() {
    return {'id': id};
  }

  factory Jose2.fromJson(Map<String, dynamic> map) {
    return Jose2(id: map['id']);
  }

  Jose2 copyWith({String? id}) {
    return Jose2(id: id ?? this.id);
  }

 static Map<String, dynamic> exampleJson() {
    return {'id': ""};
  }
}
"""

primitiveRepoTestExample = """


import 'package:either_dart/either.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:get_it/get_it.dart';
import 'package:test/model/jose.dart';
import 'package:test/repository/jose_repository.dart';
import 'package:test/service/jose_service.dart';
import 'package:mocktail/mocktail.dart';

main() {
  var repo = JoseRepository();
  var service = MockJoseService();
  var model = Jose.fromJson(Jose.exampleJson());

  setUpAll(() {
    registerFallbackValue(model);
  });

  setUp(() async {
    await GetIt.instance.reset();
    repo = JoseRepository();
    service = MockJoseService();
  });

  group('JoseRepository can', () {
    test('create', () async {
      when(() => service.set(model: model)).thenAnswer(
        (invocation) => Future(() => Right(model)),
      );

      final createResult = await repo.create(model: model);

      verify(() => service.set(model: model)).called(1);

      expect(createResult.right, model);
      expect(repo.modelCache.length, 1);
    });

    test('read', () async {
      when(() => service.read(id: any(named: 'id'))).thenAnswer(
        (invocation) => Future(() => Right(model)),
      );

      final readResult1 = await repo.read(id: model.id ?? '');
      final readResult2 = await repo.read(id: model.id ?? '');

      verify(() => service.read(id: any(named: 'id'))).called(1);

      expect(readResult1.right, readResult2.right);
    });

    test('delete', () async {
      when(() => service.delete(model: model)).thenAnswer(
            (invocation) => Future(() => Right(model)),
      );

      when(() => service.set(model: model)).thenAnswer(
            (invocation) => Future(() => Right(model)),
      );

      final createResult = await repo.create(model: model);
      expect(repo.modelCache.values.length, 1);

      final deleteResult = await repo.delete(model: model);

      verify(() => service.delete(model: model)).called(1);

      expect(repo.modelCache.values.length, 0);
      expect(deleteResult.right, model);
    });
  });
  
  test('ReadAll', () async {
      final exampleModel = Jose.fromJson(Jose.exampleJson());
      
      when(() => service.readAll()).thenAnswer(
            (invocation) => Future(() => Right([model])),
      );
      
      final readAllResult = await repo.readAll();
      expect(readAllResult.isRight, true);
      expect(readAllResult.right.length, 1);
    });
}

class MockJoseService extends Mock implements JoseService {
  MockJoseService() {
    GetIt.instance.registerSingleton<JoseService>(this);
  }
}
  

""".strip()
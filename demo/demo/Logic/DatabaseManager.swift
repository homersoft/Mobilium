//
//  DatabaseManager.swift
//  demo
//
//  Created by Grzegorz Przybyła on 20/04/2020.
//  Copyright © 2020 Silvair. All rights reserved.
//

import Foundation

class DatabaseManager {
    private let operationQueue: OperationQueue
    
    private var store: [String: String] = [:]

    init(operationQueue: OperationQueue = .init()) {
        self.operationQueue = operationQueue
    }

    func readAccountData(uid: String, onComplete: @escaping (Result<AccountDBO?, Error>) -> Void) {
        read(uid: uid, completion: onComplete)
    }

    func save<T: Encodable>(_ codable: T, for uid: String, onComplete: @escaping (Result<Void, Error>) -> Void) {
        operationQueue.addOperation { [weak self] in
            guard let self = self else { return }
            do {
                let jsonData = try JSONEncoder().encode(codable)
                let dataString = jsonData.base64EncodedString()
                self.store[uid] = dataString
                onComplete(.success(()))
            } catch {
                onComplete(.failure(error))
            }
        }
    }
    
    func read<T: Decodable>(uid: String,
                            completion: @escaping (Result<T?, Error>) -> Void) {
        guard let dataString = store[uid] else {
            completion(.success(nil))
            return
        }
        do {
            let jsonData = Data(base64Encoded: dataString) ?? Data()
            let result = try JSONDecoder().decode(T.self, from: jsonData)
            completion(.success(result))
        } catch {
            completion(.failure(error))
        }
    }
}

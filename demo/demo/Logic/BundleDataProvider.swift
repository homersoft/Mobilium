//
//  BundleDataProvider.swift
//  demo
//
//  Created by Grzegorz Przybyła on 20/04/2020.
//  Copyright © 2020 Silvair. All rights reserved.
//

import Foundation

class BundleDataProvider {
    enum Error: Swift.Error {
        case fileNotExists
        case readFileFailure
        case decodingFailure
    }
    private let operationQueue: OperationQueue
    private let jsonDecoder: JSONDecoder
    private let bundle: Bundle

    init(bundle: Bundle = .main,
         jsonDecoder: JSONDecoder = .makeWithDecodingStrategyFromSnakeCase(),
         operationQueue: OperationQueue = .init()) {
        self.bundle = bundle
        self.jsonDecoder = jsonDecoder
        self.operationQueue = operationQueue
    }

    func load<T: Decodable>(file: String, with extension: String?, onComplete: @escaping (Result<T, Error>) -> Void) {
        operationQueue.addOperation { [weak self] in
            guard let self = self else { return }
            do {
                let data = try self.getData(from: file, with: `extension`)
                let result = try self.jsonDecoder.decode(T.self, from: data)
                onComplete(.success(result))
            } catch let error as Error {
                onComplete(.failure(error))
            } catch {
                print("JSONDecoder().decode error: \(error)")
                onComplete(.failure(.decodingFailure))
            }
        }
    }

    private func finish<T: Decodable>(result: Result<T, Error>) {

    }

    private func getData(from file: String, with extension: String?) throws -> Data {
        guard let fileUrl = bundle.url(forResource: file, withExtension: `extension`) else {
            throw Error.fileNotExists
        }
        do {
            return try Data.init(contentsOf: fileUrl, options: [])
        } catch {
            print("Error: \(error)")
            throw Error.readFileFailure
        }
    }
}

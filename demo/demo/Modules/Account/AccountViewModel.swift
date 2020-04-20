//
//  AccountViewModel.swift
//  demo
//
//  Created by Grzegorz Przybyła on 20/04/2020.
//  Copyright © 2020 Silvair. All rights reserved.
//

import Foundation
import Combine

protocol AccountCoordinator: class {
    func showLoginView()
}

class AccountViewModel {
    var viewState: AnyPublisher<AccountViewState, Never> { _viewState.eraseToAnyPublisher() }
    private let currentUser: User
    private let dataManager: DatabaseManager
    private let userRepository: CurrentUserRepository
    private let coordinator: AccountCoordinator
    private let _viewState = CurrentValueSubject<AccountViewState, Never>(.initial)

    init(currentUser: User,
         coordinator: AccountCoordinator,
         userRepository: CurrentUserRepository = .init(),
         dataManager: DatabaseManager = DatabaseManager()) {
        self.currentUser = currentUser
        self.coordinator = coordinator
        self.userRepository = userRepository
        self.dataManager = dataManager
    }

    func loadData() {
        let phoneNumber = currentUser.phoneNumber ?? ""
        _viewState.send(.syncing)
        dataManager.readAccountData(uid: currentUser.identifier) { [weak self] (result) in
            switch result {
            case .success(let accountDBO?):
                self?.display(account: .init(from: accountDBO))
            case .success:
                self?._viewState.send(.loaded([.phoneNumber: phoneNumber]))
            case .failure(let error):
                self?._viewState.send(.error(title: "Ops...", message: error.localizedDescription))
            }
        }
    }

    func store(userData: [AccountField: Any?]) {
        guard let firstName = userData[.firstName] as? String,
            let lastName = userData[.lastName] as? String,
            let phoneNumber = userData[.phoneNumber] as? String,
            let email = userData[.email] as? String,
            let location = userData[.location] as? String,
            let picture = userData[.picture] as? Data else {
                _viewState.send(.validationError(title: "Ops...", message: "Please fullfill all required fields"))
                return
        }
        let account = Account(firstName: firstName, lastName: lastName, phoneNumber: phoneNumber,
                              email: email, location: location, picture: picture)

        _viewState.send(.syncing)
        dataManager.save(account.toDBO(), for: currentUser.identifier) { [weak self] result in
            switch result {
            case .success:
                self?._viewState.send(.saved)
            case .failure(let error):
                self?._viewState.send(.error(title: "Ops..", message: error.localizedDescription))
            }
        }

    }

    func logout() {
        userRepository.clear()
        coordinator.showLoginView()
    }

    private func display(account: Account) {
           let userData: [AccountField: Any] = [.firstName: account.firstName,
                                                .lastName: account.lastName,
                                                .phoneNumber: account.phoneNumber,
                                                .email: account.email,
                                                .location: account.location,
                                                .picture: account.picture]
           _viewState.send(.loaded(userData))
       }
}

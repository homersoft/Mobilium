//
//  LoginViewModel.swift
//  demo
//
//  Created by Grzegorz Przybyła on 20/04/2020.
//  Copyright © 2020 Silvair. All rights reserved.
//

import Foundation
import Combine

protocol LoginViewCoordinator: class {
    func showAccountInfo(for user: User)
}

class LoginViewModel {
    var viewState: AnyPublisher<LoginViewState, Never> { _viewState.eraseToAnyPublisher() }
    private let _viewState = CurrentValueSubject<LoginViewState, Never>(.initial)
    private let userRepository: CurrentUserRepository
    private let dataProvider: BundleDataProvider
    private let coordinator: LoginViewCoordinator

    init(coordinator: LoginViewCoordinator,
         dataProvider: BundleDataProvider = .init(),
         userRepository: CurrentUserRepository = .init()) {
        self.coordinator = coordinator
        self.dataProvider = dataProvider
        self.userRepository = userRepository
    }

    func loadCountryCodes() {
        loadCountries()
    }

    func verify(phoneNumber: String) {
        _viewState.send(.loading)
        DispatchQueue.main.asyncAfter(deadline: .now() + 1.5) { [weak self] in
            self?._viewState.send(.phoneNumberConfirmed)
        }
    }

    func confirm(verificationCode: String) {
        _viewState.send(.loading)
        DispatchQueue.main.asyncAfter(deadline: .now() + 2) { [weak self] in
            let user = User(identifier: UUID().uuidString, phoneNumber: "555111555")
            self?.userRepository.store(user: user)
            self?.coordinator.showAccountInfo(for: user)
        }
    }

    private func loadCountries()  {
        let countryCodesFile = Asset.countryCodeListFile
        dataProvider.load(file: countryCodesFile.name, with: countryCodesFile.extension) { [weak self] (result: Result<[Country], BundleDataProvider.Error>) in
            switch result {
            case .success(let countires):
                self?._viewState.send(.loaded(countires: countires))
            case .failure(let error):
                self?._viewState.send(.error(title: "Ops..", text: error.localizedDescription))
            }
        }
    }
}
